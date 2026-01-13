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


class QuranTranslator:
    """
    Translates Quran verses from Arabic/English to Urdu, Persian, and adds transliteration.
    """
    
    def __init__(
        self,
        input_json_path: str,
        output_dir: str,
        progress_file: str = "translation_progress.json",
        model_id: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    ):
        """
        Initialize the Quran Translator.
        
        Args:
            input_json_path: Path to the bilingual Quran JSON file
            output_dir: Directory to save translated chapters
            progress_file: Path to progress tracking file
            model_id: Bedrock model ID to use
        """
        self.input_json_path = input_json_path
        self.output_dir = output_dir
        self.progress_file = progress_file
        self.model_id = model_id
        
        # Initialize Bedrock client with extended timeout for large responses
        try:
            # Configure with 30 minute read timeout for large chapter translations
            config = Config(
                read_timeout=1800,  # 30 minutes in seconds
                connect_timeout=60,  # 1 minute for initial connection
                retries={'max_attempts': 0}  # We handle retries manually
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
        
        # Load or initialize progress
        self.progress = self._load_progress()
        
        # System prompt for translation
        self.system_prompt = """You are an expert translator from Arabic/English to Urdu/Persian/Transliteration. 

Your task is to translate Quran verses according to these guidelines:
1. Translate from both Arabic and English to simple, clear Urdu
2. Translate from both Arabic and English to modern, readable Persian (Farsi)
3. Provide accurate Arabic transliteration (Romanization)
4. Return ONLY a valid JSON array - no additional text or explanations
5. Preserve the exact original values for verse_number, arabic_text, and english_text
6. Ensure translations are respectful, accurate, and maintain the spiritual meaning

The output MUST be a valid JSON array with this exact structure:
[
  {
    "verse_number": <return exact original>,
    "arabic_text": "<return exact original>",
    "english_text": "<return exact original>",
    "urdu_text": "<translated from arabic + english to simple urdu>",
    "persian_text": "<translated from arabic + english to modern reading persian>",
    "transliteration": "<the transliteration from Arabic>"
  }
]"""
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress from file or initialize new progress."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                logger.info(f"Loaded progress from {self.progress_file}")
                return progress
            except Exception as e:
                logger.warning(f"Could not load progress file: {e}. Starting fresh.")
        
        return {
            "last_completed_chapter": 0,
            "last_completed_batch_in_chapter": 0,
            "chapters_completed": [],
            "total_verses_processed": 0,
            "start_time": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat()
        }
    
    def _save_progress(self):
        """Save current progress to file."""
        self.progress["last_update"] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
            logger.debug("Progress saved")
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
    
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
    
    def _create_translation_prompt(self, verses: List[Dict[str, Any]]) -> str:
        """
        Create the translation prompt for a batch of verses.
        
        Args:
            verses: List of verse dictionaries
            
        Returns:
            Formatted prompt string
        """
        verses_json = json.dumps(verses, ensure_ascii=False, indent=2)
        
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
                        "maxTokens": 8192*2
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
        Update original verses with translations (only add new fields).
        
        Args:
            original_verses: Original verse dictionaries
            translated_verses: Translated verse dictionaries from Bedrock
            
        Returns:
            Updated verse dictionaries
        """
        updated_verses = []
        
        for orig, trans in zip(original_verses, translated_verses):
            # Start with original verse (preserves all original data)
            updated = orig.copy()
            
            # Add only the new translation fields
            if 'urdu_text' in trans:
                updated['urdu_text'] = trans['urdu_text']
            if 'persian_text' in trans:
                updated['persian_text'] = trans['persian_text']
            if 'transliteration' in trans:
                updated['transliteration'] = trans['transliteration']
            
            updated_verses.append(updated)
        
        return updated_verses
    
    def _save_batch(self, chapter_number: int, batch_idx: int, verses: List[Dict[str, Any]]):
        """
        Save a batch of translated verses to interim storage.
        
        Args:
            chapter_number: Chapter number
            batch_idx: Batch index
            verses: List of translated verse dictionaries
        """
        batch_filename = f"chapter_{chapter_number:03d}_batch_{batch_idx:04d}.json"
        batch_filepath = os.path.join(self.interim_dir, batch_filename)
        
        try:
            with open(batch_filepath, 'w', encoding='utf-8') as f:
                json.dump(verses, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved batch {batch_idx} to interim storage: {batch_filename}")
        except Exception as e:
            logger.error(f"Failed to save batch to interim storage: {e}")
            # Non-critical - log but don't raise
    
    def _load_interim_batches(self, chapter_number: int, total_verses: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Load any existing interim batches for a chapter.
        
        Args:
            chapter_number: Chapter number
            total_verses: Total number of verses in chapter
            
        Returns:
            Dictionary mapping batch_idx to list of verses
        """
        batches = {}
        pattern = f"chapter_{chapter_number:03d}_batch_*.json"
        
        try:
            for filename in os.listdir(self.interim_dir):
                if filename.startswith(f"chapter_{chapter_number:03d}_batch_") and filename.endswith('.json'):
                    # Extract batch index from filename
                    batch_idx_str = filename.replace(f"chapter_{chapter_number:03d}_batch_", "").replace(".json", "")
                    batch_idx = int(batch_idx_str)
                    
                    filepath = os.path.join(self.interim_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        verses = json.load(f)
                    
                    batches[batch_idx] = verses
                    logger.debug(f"Loaded interim batch {batch_idx} with {len(verses)} verses")
            
            if batches:
                logger.info(f"Loaded {len(batches)} interim batches for chapter {chapter_number}")
        except Exception as e:
            logger.warning(f"Failed to load interim batches: {e}")
        
        return batches
    
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
        
        # Load any existing interim batches
        interim_batches = self._load_interim_batches(chapter_number, total_verses)
        
        # Determine starting batch based on progress
        start_batch = 0
        if self.progress.get('last_completed_chapter') == chapter_number:
            start_batch = self.progress.get('last_completed_batch_in_chapter', 0) + 1
            logger.info(f"Resuming from batch {start_batch}")
        
        # Process verses in batches
        updated_verses = verses.copy()
        
        # First, restore any existing interim batches
        for batch_idx, batch_verses in interim_batches.items():
            start_idx = batch_idx * batch_size
            for i, verse in enumerate(batch_verses):
                if start_idx + i < len(updated_verses):
                    updated_verses[start_idx + i] = verse
            logger.info(f"Restored batch {batch_idx} from interim storage")
        
        for batch_idx in range(start_batch, (total_verses + batch_size - 1) // batch_size):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, total_verses)
            batch_verses = verses[start_idx:end_idx]
            
            logger.info(
                f"Processing chapter {chapter_number}, batch {batch_idx + 1}, "
                f"verses {start_idx + 1}-{end_idx} of {total_verses}"
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
                
                # Update the verses list
                for i, updated_verse in enumerate(updated_batch):
                    updated_verses[start_idx + i] = updated_verse
                
                # Save batch to interim storage
                self._save_batch(chapter_number, batch_idx, updated_batch)
                
                # Update progress
                self.progress['last_completed_chapter'] = chapter_number
                self.progress['last_completed_batch_in_chapter'] = batch_idx
                self.progress['total_verses_processed'] += len(batch_verses)
                self._save_progress()
                
                logger.info(f"Batch {batch_idx + 1} completed successfully")
                
                # Small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to process batch {batch_idx + 1}: {e}")
                logger.error("Progress saved. You can resume by running the script again.")
                raise
        
        # Update chapter data with translated verses
        updated_chapter = chapter_data.copy()
        updated_chapter['verses'] = updated_verses
        
        logger.info(f"Completed chapter {chapter_number}: {chapter_name}")
        return updated_chapter
    
    def translate_all_chapters(self, chapters_to_process: Optional[Set[int]] = None):
        """
        Main method to translate all chapters in the Quran.
        
        Args:
            chapters_to_process: Optional set of specific chapter numbers to process.
                                If None, processes all chapters.
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
        
        # Determine starting chapter
        start_chapter_num = self.progress.get('last_completed_chapter', 0)
        if start_chapter_num in self.progress.get('chapters_completed', []):
            start_chapter_num += 1
        
        # Process each chapter
        for chapter_key in chapter_keys:
            chapter_data = quran_data[chapter_key]
            chapter_number = chapter_data['chapter_number']
            
            # Skip if not in the list of chapters to process
            if chapters_to_process and chapter_number not in chapters_to_process:
                logger.debug(f"Skipping chapter {chapter_number} (not in target list)")
                continue
            
            # Skip if already completed
            if chapter_number in self.progress.get('chapters_completed', []):
                logger.info(f"Skipping chapter {chapter_number} (already completed)")
                continue
            
            try:
                # Translate chapter
                updated_chapter = self.translate_chapter(chapter_key, chapter_data)
                
                # Save chapter
                self._save_chapter(chapter_key, updated_chapter)
                
                # Mark chapter as completed
                if 'chapters_completed' not in self.progress:
                    self.progress['chapters_completed'] = []
                self.progress['chapters_completed'].append(chapter_number)
                self.progress['last_completed_batch_in_chapter'] = 0
                self._save_progress()
                
                logger.info(f"Chapter {chapter_number} completed and saved")
                
            except Exception as e:
                logger.error(f"Failed to process chapter {chapter_number}: {e}")
                logger.error("Translation stopped. Progress saved. Run again to resume.")
                return
        
        logger.info("=" * 80)
        logger.info("Translation Complete!")
        logger.info(f"Total verses processed: {self.progress['total_verses_processed']}")
        logger.info(f"Total chapters completed: {len(self.progress['chapters_completed'])}")
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
    PROGRESS_FILE = "/home/sazmham/personal_apps/abjad/abjad_calculator/apps/dad_english_quran_converter/translation_progress.json"
    
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
        '--progress',
        type=str,
        default=PROGRESS_FILE,
        help=f'Progress tracking file (default: {PROGRESS_FILE})'
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
            output_dir=args.output,
            progress_file=args.progress
        )
        
        translator.translate_all_chapters(chapters_to_process)
        
    except KeyboardInterrupt:
        logger.info("\nTranslation interrupted by user. Progress has been saved.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Translation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
