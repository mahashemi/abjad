#!/usr/bin/env python3
"""
Quran Translation Script - Translates Arabic/English verses to Urdu, Persian, and Transliteration

This script processes the Quran bilingual JSON file and uses Claude Sonnet via AWS Bedrock
to translate verses into Urdu, Persian, and add transliteration. It processes 10 verses at
a time and includes robust error handling and resume capability.

Features:
- Batch processing (10 verses at a time)
- Progress tracking with resume capability
- Error handling with automatic retry logic
- Saves each chapter as a Python file
- Only updates new fields (preserves original data)
"""

import json
import os
import sys
import time
import boto3
from botocore.config import Config
import argparse
from typing import List, Dict, Any, Optional, Tuple, Set
from pathlib import Path
import logging
from datetime import datetime
import glob
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quran_translation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 5

class QuranTranslator:
    """
    Translates Quran verses from Arabic/English to Urdu, Persian, and adds transliteration.
    """
    
    def __init__(
        self,
        input_json_path: str,
        output_dir: str,
        model_id: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        quran_library_path: Optional[str] = None
    ):
        """
        Initialize the Quran Translator.
        
        Args:
            input_json_path: Path to the bilingual Quran JSON file
            output_dir: Directory to save translated chapters
            model_id: Bedrock model ID to use
            quran_library_path: Path to quran_library directory. If None, will auto-detect
                               relative to input_json_path (../../quran_library)
        """
        self.input_json_path = input_json_path
        self.output_dir = output_dir
        self.model_id = model_id
        
        # Determine quran_library path
        if quran_library_path:
            self.quran_library_path = str(Path(quran_library_path).resolve())
        else:
            # Auto-detect: quran_library is at ../../quran_library relative to input JSON
            json_path = Path(input_json_path).resolve()
            self.quran_library_path = str(json_path.parent.parent.parent / 'quran_library')
        
        logger.info(f"Quran library path: {self.quran_library_path}")
        
        # Initialize Bedrock client with extended timeout for large responses
        try:
            # Configure with 30 minute read timeout for large chapter translations
            config = Config(
                read_timeout=1800,  # 30 minutes in seconds
                connect_timeout=60,  # 1 minute for initial connection
                retries={'max_attempts': 3}  # We handle retries manually
            )
            self.bedrock_client = boto3.client('bedrock-runtime', config=config)
            logger.info("Bedrock client initialized successfully (read timeout: 30 minutes)")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {output_dir}")
        
        # Create interim batches directory for storing progress
        self.interim_dir = os.path.join(output_dir, ".interim_batches")
        Path(self.interim_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Interim batches directory: {self.interim_dir}")
        
        # System prompt for translation
        self.system_prompt = """You are an expert translator from Arabic/English to Urdu/Persian/Transliteration. 

Your task is to translate Quran verses according to these guidelines:
1. Translate from both Arabic and English to simple, clear Urdu
2. Translate from both Arabic and English to modern, readable Persian (Farsi)
3. Provide accurate Arabic transliteration (Romanization)
4. Return ONLY a valid JSON array - no additional text, explanations, or markdown
5. Preserve the exact original values for verse_number, arabic_text, and english_text
6. Ensure translations are respectful, accurate, and maintain the spiritual meaning
7. CRITICAL: Return valid JSON only - no trailing commas, proper escaping, proper quotes

OUTPUT SCHEMA:
You MUST return a JSON array matching this exact schema:

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["verse_number", "arabic_text", "english_text", "urdu_text", "persian_text", "transliteration"],
    "properties": {
      "verse_number": {
        "type": "integer",
        "description": "Exact original verse number (do not modify)"
      },
      "arabic_text": {
        "type": "string",
        "description": "Exact original Arabic text (do not modify)"
      },
      "english_text": {
        "type": "string",
        "description": "Exact original English text (do not modify)"
      },
      "urdu_text": {
        "type": "string",
        "description": "Translation to simple, clear Urdu from given English+Arabic"
      },
      "persian_text": {
        "type": "string",
        "description": "Translation to modern, readable Persian (Farsi) from given English+Arabic"
      },
      "transliteration": {
        "type": "string",
        "description": "Arabic text romanization/transliteration"
      }
    },
    "additionalProperties": false
  }
}

EXAMPLE OUTPUT FORMAT:
[
  {
    "verse_number": 1,
    "arabic_text": "بِسْمِ اللّٰهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "english_text": "In the name of Allah, the Most Gracious, the Most Merciful",
    "urdu_text": "اللہ کے نام سے جو بڑا مہربان نہایت رحم والا ہے",
    "persian_text": "به نام خداوند بخشنده مهربان",
    "transliteration": "Bismillah ir-Rahman ir-Rahim"
  },
  ...
]

Remember: Return ONLY the JSON array with no additional text before or after it."""
    
    def _get_completed_verses_from_interim(self, chapter_number: int) -> Set[int]:
        """
        Scan interim batch files to find which verses have already been translated.
        
        Args:
            chapter_number: Chapter number
            
        Returns:
            Set of verse numbers that have been completed
        """
        completed_verses = set()
        
        try:
            for filename in os.listdir(self.interim_dir):
                if filename.startswith(f"chapter_{chapter_number:03d}_batch_") and filename.endswith('.json'):
                    filepath = os.path.join(self.interim_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        verses = json.load(f)
                    
                    for verse in verses:
                        if 'verse_number' in verse:
                            completed_verses.add(verse['verse_number'])
            
            if completed_verses:
                logger.info(f"Found {len(completed_verses)} already translated verses for chapter {chapter_number}")
                logger.debug(f"Completed verses: {sorted(completed_verses)}")
        except Exception as e:
            logger.warning(f"Failed to scan interim batches: {e}")
        
        return completed_verses
    
    def _get_completed_chapters(self) -> Set[int]:
        """
        Get list of chapters that have been fully completed (have output files).
        
        Returns:
            Set of completed chapter numbers
        """
        completed = set()
        
        try:
            for filename in os.listdir(self.output_dir):
                if filename.startswith('chapter_') and filename.endswith('.py'):
                    # Extract chapter number from filename like "chapter_002_baqara.py"
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        try:
                            chapter_num = int(parts[1])
                            completed.add(chapter_num)
                        except ValueError:
                            pass
            
            if completed:
                logger.info(f"Found {len(completed)} completed chapters: {sorted(completed)}")
        except Exception as e:
            logger.warning(f"Failed to scan for completed chapters: {e}")
        
        return completed
    
    def _load_quran_data(self) -> Dict[str, Any]:
        """Load the bilingual Quran JSON file."""
        try:
            with open(self.input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded Quran data with {len(data)} chapters")
            return data
        except Exception as e:
            logger.error(f"Failed to load Quran data: {e}")
            raise
    
    def _load_arabic_from_library(self, chapter_number: int) -> Dict[int, str]:
        """
        Load Arabic text from quran_library for a chapter.
        
        Args:
            chapter_number: Chapter number to load
            
        Returns:
            Dictionary mapping verse_number to arabic_text
        """
        try:
            # Find the matching file for this chapter
            pattern = f"{self.quran_library_path}/chapter_{chapter_number:03d}_*.py"
            matches = glob.glob(pattern)
            
            if not matches:
                logger.warning(f"No quran_library file found for chapter {chapter_number}, using JSON arabic text")
                return {}
            
            chapter_file = matches[0]
            logger.debug(f"Loading Arabic text from: {chapter_file}")
            
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location("chapter_module", chapter_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Extract arabic_text by verse_number (convert to int for consistent comparison)
            arabic_dict = {}
            for ayat in module.ayats:
                verse_num = ayat['verse_number']
                # Convert to int if it's a string
                if isinstance(verse_num, str):
                    verse_num = int(verse_num)
                arabic_dict[verse_num] = ayat['arabic_text']
            
            logger.info(f"Loaded {len(arabic_dict)} verses' Arabic text from quran_library for chapter {chapter_number}")
            return arabic_dict
            
        except Exception as e:
            logger.warning(f"Failed to load Arabic text from quran_library for chapter {chapter_number}: {e}")
            logger.warning("Will use Arabic text from JSON file instead")
            return {}
    
    def _create_translation_prompt(self, verses: List[Dict[str, Any]]) -> str:
        """
        Create the translation prompt for a batch of verses.
        
        Args:
            verses: List of verse dictionaries
            
        Returns:
            Formatted prompt string
        """
        
        verses_json = json.dumps(verses, ensure_ascii=False, indent=2)
        logging.info(f"Loaded {len(verses)} verses, char len {len(verses_json)}")
        
        prompt = f"""Please translate the following Quran verses. Return ONLY a valid JSON array with no additional text.

Input verses:
```
{verses_json}
```

Remember:
- Return exact original values for verse_number, arabic_text, and english_text
- Add urdu_text (simple Urdu translation)
- Add persian_text (modern Persian/Farsi translation)
- Add transliteration (Arabic Romanization)
- Return ONLY the JSON array, nothing else"""
        
        return prompt
    
    def _call_bedrock(
        self,
        prompt: str,
        max_retries: int = 3,
        retry_delay: int = 5
    ) -> str:
        """
        Call Bedrock API with retry logic.
        
        Args:
            prompt: The prompt to send
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
            
        Returns:
            Generated text from Bedrock
            
        Raises:
            RuntimeError: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                logger.debug(f"Calling Bedrock (attempt {attempt + 1}/{max_retries})")
                
                response = self.bedrock_client.converse(
                    modelId=self.model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": [{"text": prompt}]
                        }
                    ],
                    system=[{"text": self.system_prompt}],
                    inferenceConfig={
                        "temperature": 0.1,
                        "maxTokens": 24000
                    }
                )
                
                generated_text = response['output']['message']['content'][0]['text']
                
                # Log usage
                usage = response.get('usage', {})
                logger.debug(
                    f"Bedrock usage - Input: {usage.get('inputTokens', 0)}, "
                    f"Output: {usage.get('outputTokens', 0)}, "
                    f"Total: {usage.get('totalTokens', 0)}"
                )
                
                return generated_text
                
            except Exception as e:
                logger.warning(f"Bedrock call failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("All Bedrock retry attempts failed")
                    raise RuntimeError(f"Bedrock API call failed after {max_retries} attempts: {e}")
    
    def _parse_translation_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse the translation response from Bedrock.
        
        Args:
            response_text: Raw response text from Bedrock
            
        Returns:
            List of translated verse dictionaries
            
        Raises:
            ValueError: If parsing fails
        """
        try:
            # Clean the response
            cleaned = response_text.strip()
            
            # Find JSON array boundaries
            start_idx = cleaned.find('[')
            end_idx = cleaned.rfind(']')
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("No JSON array found in response")
            
            json_text = cleaned[start_idx:end_idx + 1]
            
            # Parse JSON
            verses = json.loads(json_text)
            
            if not isinstance(verses, list):
                raise ValueError("Expected a JSON array")
            
            logger.debug(f"Successfully parsed {len(verses)} verses")
            return verses
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.debug(f"Response text: {response_text[:500]}...")
            raise ValueError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            logger.error(f"Response parsing failed: {e}")
            raise
    
    def _update_verses_with_translations(
        self,
        original_verses: List[Dict[str, Any]],
        translated_verses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Update original verses with translations by matching on verse_number.
        CRITICAL: Matches by verse_number to ensure correct pairing, not by position.
        
        Args:
            original_verses: Original verse dictionaries
            translated_verses: Translated verse dictionaries from Bedrock
            
        Returns:
            Updated verse dictionaries
        """
        # Create a mapping of verse_number to translated data for safe matching
        trans_by_verse = {v['verse_number']: v for v in translated_verses}
        
        updated_verses = []
        
        for orig in original_verses:
            # Start with original verse (preserves all original data)
            updated = orig.copy()
            
            verse_num = orig['verse_number']
            
            # Find matching translation by verse_number (not by position!)
            if verse_num in trans_by_verse:
                trans = trans_by_verse[verse_num]
                
                # Add only the new translation fields
                if 'urdu_text' in trans:
                    updated['urdu_text'] = trans['urdu_text']
                if 'persian_text' in trans:
                    updated['persian_text'] = trans['persian_text']
                if 'transliteration' in trans:
                    updated['transliteration'] = trans['transliteration']
            else:
                logger.warning(f"No translation found for verse {verse_num}")
            
            updated_verses.append(updated)
        
        return updated_verses
    
    def _save_batch(self, chapter_number: int, verse_numbers: List[int], verses: List[Dict[str, Any]]):
        """
        Save a batch of translated verses to interim storage.
        Uses verse numbers to create unique batch filename.
        
        Args:
            chapter_number: Chapter number
            verse_numbers: List of verse numbers in this batch
            verses: List of translated verse dictionaries
        """
        # Create filename based on verse range for better clarity
        min_verse = min(verse_numbers)
        max_verse = max(verse_numbers)
        batch_filename = f"chapter_{chapter_number:03d}_batch_v{min_verse:04d}_v{max_verse:04d}.json"
        batch_filepath = os.path.join(self.interim_dir, batch_filename)
        
        try:
            with open(batch_filepath, 'w', encoding='utf-8') as f:
                json.dump(verses, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved batch verses {min_verse}-{max_verse} to interim storage: {batch_filename}")
        except Exception as e:
            logger.error(f"Failed to save batch to interim storage: {e}")
            # Non-critical - log but don't raise
    
    def _load_completed_verses_from_interim(self, chapter_number: int) -> Dict[int, Dict[str, Any]]:
        """
        Load all completed verses from interim batches for a chapter.
        
        Args:
            chapter_number: Chapter number
            
        Returns:
            Dictionary mapping verse_number to verse data
        """
        completed_verses = {}
        
        try:
            for filename in os.listdir(self.interim_dir):
                if filename.startswith(f"chapter_{chapter_number:03d}_batch_") and filename.endswith('.json'):
                    filepath = os.path.join(self.interim_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        verses = json.load(f)
                    
                    for verse in verses:
                        verse_num = verse.get('verse_number')
                        if verse_num is not None:
                            completed_verses[verse_num] = verse
            
            if completed_verses:
                logger.info(f"Loaded {len(completed_verses)} completed verses from interim storage for chapter {chapter_number}")
        except Exception as e:
            logger.warning(f"Failed to load interim batches: {e}")
        
        return completed_verses
    
    def _clear_interim_batches(self, chapter_number: int):
        """
        Clear interim batch files for a completed chapter.
        
        Args:
            chapter_number: Chapter number
        """
        try:
            for filename in os.listdir(self.interim_dir):
                if filename.startswith(f"chapter_{chapter_number:03d}_batch_"):
                    filepath = os.path.join(self.interim_dir, filename)
                    os.remove(filepath)
            logger.debug(f"Cleared interim batches for chapter {chapter_number}")
        except Exception as e:
            logger.warning(f"Failed to clear interim batches: {e}")
    
    def _save_chapter(self, chapter_key: str, chapter_data: Dict[str, Any]):
        """
        Save a chapter as a Python file with ayats variable.
        
        Args:
            chapter_key: Chapter key (e.g., "1:Fatiha:7")
            chapter_data: Complete chapter data
        """
        chapter_number = chapter_data['chapter_number']
        chapter_name = chapter_data['chapter_name'].lower().replace(" ","_")
        
        # Create filename
        filename = f"chapter_{chapter_number:03d}_{chapter_name}.py"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f'"""\n')
                f.write(f'Chapter {chapter_number}: {chapter_name}\n')
                f.write(f'Arabic: {chapter_data["chapter_name_arabic"]}\n')
                f.write(f'Total Verses: {chapter_data["total_verses"]}\n')
                f.write(f'Generated: {datetime.now().isoformat()}\n')
                f.write(f'"""\n\n')
                f.write('ayats = ')
                f.write(json.dumps(chapter_data['verses'], indent=2, ensure_ascii=False))
                f.write('\n')
            
            logger.info(f"Saved chapter {chapter_number} to {filepath}")
            
            # Clear interim batches after successful chapter save
            self._clear_interim_batches(chapter_number)
            
        except Exception as e:
            logger.error(f"Failed to save chapter {chapter_number}: {e}")
            raise
    
    def translate_chapter(
        self,
        chapter_key: str,
        chapter_data: Dict[str, Any],
        batch_size: int = 10
    ) -> Dict[str, Any]:
        """
        Translate all verses in a chapter.
        
        Args:
            chapter_key: Chapter key from JSON
            chapter_data: Chapter data dictionary
            batch_size: Number of verses to process at once
            
        Returns:
            Updated chapter data with translations
        """
        chapter_number = chapter_data['chapter_number']
        chapter_name = chapter_data['chapter_name']
        verses = chapter_data['verses']
        total_verses = len(verses)
        
        logger.info(f"Starting chapter {chapter_number}: {chapter_name} ({total_verses} verses)")
        
        # Load Arabic text from quran_library
        arabic_from_library = self._load_arabic_from_library(chapter_number)
        
        # Replace Arabic text in verses if available from library
        verses_with_library_arabic = []
        for verse in verses:
            verse_copy = verse.copy()
            verse_num = verse['verse_number']
            if verse_num in arabic_from_library:
                verse_copy['arabic_text'] = arabic_from_library[verse_num]
                logger.debug(f"Using Arabic text from library for verse {verse_num}")
            verses_with_library_arabic.append(verse_copy)
        
        # Use verses with library Arabic text for processing
        verses = verses_with_library_arabic
        
        # Load already completed verses from interim storage
        completed_verses_dict = self._load_completed_verses_from_interim(chapter_number)
        completed_verse_numbers = set(completed_verses_dict.keys())
        
        # Create a mapping of verse_number to verse for easy lookup
        verse_by_number = {v['verse_number']: v for v in verses}
        
        # Start with original verses, then update with completed ones
        updated_verses = verses.copy()
        for i, verse in enumerate(updated_verses):
            verse_num = verse['verse_number']
            if verse_num in completed_verses_dict:
                updated_verses[i] = completed_verses_dict[verse_num]
                logger.debug(f"Restored completed verse {verse_num} from interim storage")
        
        # Identify verses that still need translation
        verses_to_translate = [v for v in verses if v['verse_number'] not in completed_verse_numbers]
        
        if not verses_to_translate:
            logger.info(f"All verses for chapter {chapter_number} already translated!")
        else:
            logger.info(f"Need to translate {len(verses_to_translate)} verses (out of {total_verses})")
        
        # Process remaining verses in batches
        for batch_idx in range(0, len(verses_to_translate), batch_size):
            batch_verses = verses_to_translate[batch_idx:batch_idx + batch_size]
            batch_verse_numbers = [v['verse_number'] for v in batch_verses]
            
            logger.info(
                f"Processing chapter {chapter_number}, batch {batch_idx // batch_size + 1}, "
                f"verses {batch_verse_numbers[0]}-{batch_verse_numbers[-1]} "
                f"({len(verses_to_translate) - batch_idx - len(batch_verses)} remaining)"
            )
            
            try:
                # Create prompt
                prompt = self._create_translation_prompt(batch_verses)
                
                # Call Bedrock
                response_text = self._call_bedrock(prompt)
                
                # Parse response
                translated_batch = self._parse_translation_response(response_text)
                
                # Validate batch size
                if len(translated_batch) != len(batch_verses):
                    raise ValueError(
                        f"Response has {len(translated_batch)} verses but expected {len(batch_verses)}"
                    )
                
                # Update verses with translations
                updated_batch = self._update_verses_with_translations(batch_verses, translated_batch)
                
                # Update the verses list by matching verse numbers
                for updated_verse in updated_batch:
                    verse_num = updated_verse['verse_number']
                    # Find and update the verse in updated_verses list
                    for i, v in enumerate(updated_verses):
                        if v['verse_number'] == verse_num:
                            updated_verses[i] = updated_verse
                            break
                
                # Save batch to interim storage
                self._save_batch(chapter_number, batch_verse_numbers, updated_batch)
                
                logger.info(f"Batch completed successfully - translated verses {batch_verse_numbers[0]}-{batch_verse_numbers[-1]}")
                
                # Small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to process batch with verses {batch_verse_numbers[0]}-{batch_verse_numbers[-1]}: {e}")
                logger.error("Interim batches saved. You can resume by running the script again.")
                raise
        
        # Update chapter data with translated verses
        updated_chapter = chapter_data.copy()
        updated_chapter['verses'] = updated_verses
        
        logger.info(f"Completed chapter {chapter_number}: {chapter_name}")
        return updated_chapter
    
    def translate_all_chapters(self, chapters_to_process: Optional[Set[int]] = None, batch_size: int = 5):
        """
        Main method to translate all chapters in the Quran.
        
        Args:
            chapters_to_process: Optional set of specific chapter numbers to process.
                                If None, processes all chapters.
            batch_size: Number of verses to process in one batch (default: 5)
        """
        logger.info("=" * 80)
        logger.info("Starting Quran Translation")
        logger.info("=" * 80)
        
        # Load Quran data
        quran_data = self._load_quran_data()
        
        # Get sorted chapter keys
        chapter_keys = sorted(
            quran_data.keys(),
            key=lambda x: int(x.split(':')[0])
        )
        
        total_chapters = len(chapter_keys)
        logger.info(f"Total chapters in Quran: {total_chapters}")
        
        if chapters_to_process:
            logger.info(f"Chapters to process: {sorted(chapters_to_process)}")
            logger.info(f"Total chapters to process: {len(chapters_to_process)}")
        
        logger.info(f"Batch size: {batch_size} verses per batch")
        
        # Get list of already completed chapters
        completed_chapters = self._get_completed_chapters()
        
        # Process each chapter
        for chapter_key in chapter_keys:
            chapter_data = quran_data[chapter_key]
            chapter_number = chapter_data['chapter_number']
            
            # Skip if not in the list of chapters to process
            if chapters_to_process and chapter_number not in chapters_to_process:
                logger.debug(f"Skipping chapter {chapter_number} (not in target list)")
                continue
            
            # Skip if already completed (has output file)
            if chapter_number in completed_chapters:
                logger.info(f"Skipping chapter {chapter_number} (already completed)")
                continue
            
            try:
                # Translate chapter
                updated_chapter = self.translate_chapter(chapter_key, chapter_data, batch_size=batch_size)
                
                # Save chapter
                self._save_chapter(chapter_key, updated_chapter)
                
                logger.info(f"Chapter {chapter_number} completed and saved")
                
            except Exception as e:
                logger.error(f"Failed to process chapter {chapter_number}: {e}")
                logger.error("Translation stopped. Progress saved. Run again to resume.")
                return
        
        # Count final results
        final_completed = self._get_completed_chapters()
        logger.info("=" * 80)
        logger.info("Translation Complete!")
        logger.info(f"Total chapters completed: {len(final_completed)}")
        logger.info(f"Completed chapters: {sorted(final_completed)}")
        logger.info("=" * 80)


def parse_chapter_ranges(range_str: str) -> Set[int]:
    """
    Parse chapter range string into a set of chapter numbers.
    
    Supports formats:
    - Single chapter: "15"
    - Range: "15-54"
    - Multiple ranges: "15-54,60-77"
    - Mixed: "15,17-20,25"
    
    Args:
        range_str: String containing chapter numbers/ranges
        
    Returns:
        Set of chapter numbers
    """
    chapters = set()
    parts = range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range
            start, end = part.split('-')
            start_num = int(start.strip())
            end_num = int(end.strip())
            chapters.update(range(start_num, end_num + 1))
        else:
            # Single chapter
            chapters.add(int(part))
    
    return chapters


def main():
    """Main entry point."""
    # Configuration
    INPUT_JSON = "/home/sazmham/personal_apps/abjad/abjad_calculator/apps/dad_english_quran_converter/quran_bilingual.json"
    OUTPUT_DIR = "/home/sazmham/personal_apps/abjad/abjad_calculator/apps/dad_english_quran_converter/translated_chapters"
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Translate Quran verses from Arabic/English to Urdu, Persian, and Transliteration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single chapter
  python quran_translator.py --chapter 15
  
  # Process a range of chapters
  python quran_translator.py --chapters 15-54
  
  # Process multiple ranges
  python quran_translator.py --chapters 15-54,60-77
  
  # Process specific chapters, excluding some
  python quran_translator.py --chapters 15-77 --exclude 55,56,58,59
  
  # Process all remaining chapters (default)
  python quran_translator.py
        """
    )
    
    parser.add_argument(
        '--chapter',
        type=int,
        help='Process a single chapter (e.g., --chapter 15)'
    )
    
    parser.add_argument(
        '--chapters',
        type=str,
        help='Process specific chapters or ranges (e.g., --chapters 15-54,60-77)'
    )
    
    parser.add_argument(
        '--exclude',
        type=str,
        help='Exclude specific chapters or ranges (e.g., --exclude 55,56,58,59)'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default=INPUT_JSON,
        help=f'Path to input JSON file (default: {INPUT_JSON})'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=OUTPUT_DIR,
        help=f'Output directory for translated chapters (default: {OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=5,
        help=f'Number of verses to process in one batch (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Determine which chapters to process
    chapters_to_process = None
    
    if args.chapter:
        # Single chapter
        chapters_to_process = {args.chapter}
        logger.info(f"Processing single chapter: {args.chapter}")
    elif args.chapters:
        # Parse chapter ranges
        chapters_to_process = parse_chapter_ranges(args.chapters)
        logger.info(f"Processing chapters: {sorted(chapters_to_process)}")
    
    # Handle exclusions
    if args.exclude:
        exclude_chapters = parse_chapter_ranges(args.exclude)
        if chapters_to_process:
            chapters_to_process -= exclude_chapters
            logger.info(f"Excluding chapters: {sorted(exclude_chapters)}")
            logger.info(f"Final chapter list: {sorted(chapters_to_process)}")
        else:
            logger.warning("--exclude specified but no --chapters specified. Exclusions will be ignored.")
    
    try:
        translator = QuranTranslator(
            input_json_path=args.input,
            output_dir=args.output
        )
        
        translator.translate_all_chapters(chapters_to_process, batch_size=args.batch_size)
        
    except KeyboardInterrupt:
        logger.info("\nTranslation interrupted by user. Progress has been saved.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Translation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
