#!/usr/bin/env python3
"""
Sync Quran JSON with Library Script

This script updates the quran_bilingual.json file's Arabic text with the latest 
Arabic text from the quran_library files. This keeps the JSON file synchronized 
with any corrections or updates made to the Arabic text in quran_library.

Usage:
    python sync_json_with_library.py
    python sync_json_with_library.py --json-path /path/to/quran_bilingual.json
    python sync_json_with_library.py --library-path /path/to/quran_library
"""

import json
import glob
import importlib.util
import argparse
from pathlib import Path
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def load_arabic_from_library_file(chapter_file: str) -> Dict[int, str]:
    """
    Load Arabic text from a quran_library chapter file.
    
    Args:
        chapter_file: Path to the chapter file
        
    Returns:
        Dictionary mapping verse_number to arabic_text
    """
    try:
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
        
        return arabic_dict
        
    except Exception as e:
        logger.error(f"Failed to load {chapter_file}: {e}")
        return {}


def sync_json_with_library(json_path: str, library_path: str) -> None:
    """
    Sync the JSON file's Arabic text with quran_library files.
    
    Args:
        json_path: Path to the quran_bilingual.json file
        library_path: Path to the quran_library directory
    """
    # Load the JSON file
    logger.info(f"Loading JSON file: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
        logger.info(f"Loaded {len(quran_data)} chapters from JSON")
    except Exception as e:
        logger.error(f"Failed to load JSON file: {e}")
        return
    
    # Track statistics
    chapters_updated = 0
    verses_updated = 0
    chapters_not_found = []
    
    # Process each chapter in the JSON
    for chapter_key, chapter_data in quran_data.items():
        chapter_number = chapter_data['chapter_number']
        chapter_name = chapter_data['chapter_name']
        
        # Find the corresponding quran_library file
        pattern = f"{library_path}/chapter_{chapter_number:03d}_*.py"
        matches = glob.glob(pattern)
        
        if not matches:
            logger.warning(f"No quran_library file found for chapter {chapter_number}: {chapter_name}")
            chapters_not_found.append(chapter_number)
            continue
        
        chapter_file = matches[0]
        logger.info(f"Processing chapter {chapter_number}: {chapter_name}")
        
        # Load Arabic text from library
        arabic_from_library = load_arabic_from_library_file(chapter_file)
        
        if not arabic_from_library:
            logger.warning(f"Could not load Arabic text from {chapter_file}")
            continue
        
        # Update verses in JSON with library Arabic text
        chapter_updated = False
        for verse in chapter_data['verses']:
            verse_num = verse['verse_number']
            if verse_num in arabic_from_library:
                old_arabic = verse.get('arabic_text', '')
                new_arabic = arabic_from_library[verse_num]
                
                if old_arabic != new_arabic:
                    verse['arabic_text'] = new_arabic
                    verses_updated += 1
                    chapter_updated = True
                    logger.debug(f"Updated verse {verse_num} Arabic text")
        
        if chapter_updated:
            chapters_updated += 1
            logger.info(f"Chapter {chapter_number} updated")
    
    # Save the updated JSON
    logger.info("Saving updated JSON file...")
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(quran_data, f, indent=2, ensure_ascii=False)
        logger.info("JSON file saved successfully")
    except Exception as e:
        logger.error(f"Failed to save JSON file: {e}")
        return
    
    # Print summary
    logger.info("=" * 60)
    logger.info("SYNC SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total chapters in JSON: {len(quran_data)}")
    logger.info(f"Chapters updated: {chapters_updated}")
    logger.info(f"Verses updated: {verses_updated}")
    if chapters_not_found:
        logger.warning(f"Chapters not found in library: {chapters_not_found}")
    logger.info("=" * 60)


def main():
    """Main entry point."""
    # Default paths
    DEFAULT_JSON = "/home/sazmham/personal_apps/abjad/abjad_calculator/apps/dad_english_quran_converter/quran_bilingual.json"
    DEFAULT_LIBRARY = "/home/sazmham/personal_apps/abjad/abjad_calculator/quran_library"
    
    parser = argparse.ArgumentParser(
        description='Sync quran_bilingual.json Arabic text with quran_library files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default paths
  python sync_json_with_library.py
  
  # Specify custom JSON path
  python sync_json_with_library.py --json-path /path/to/quran_bilingual.json
  
  # Specify custom library path
  python sync_json_with_library.py --library-path /path/to/quran_library
  
  # Specify both paths
  python sync_json_with_library.py --json-path /path/to/json --library-path /path/to/library
        """
    )
    
    parser.add_argument(
        '--json-path',
        type=str,
        default=DEFAULT_JSON,
        help=f'Path to quran_bilingual.json file (default: {DEFAULT_JSON})'
    )
    
    parser.add_argument(
        '--library-path',
        type=str,
        default=DEFAULT_LIBRARY,
        help=f'Path to quran_library directory (default: {DEFAULT_LIBRARY})'
    )
    
    args = parser.parse_args()
    
    # Auto-detect library path if using default JSON path
    if args.json_path == DEFAULT_JSON and args.library_path == DEFAULT_LIBRARY:
        # Use relative path detection
        json_path = Path(args.json_path).resolve()
        library_path = str(json_path.parent.parent.parent / 'quran_library')
        logger.info(f"Auto-detected library path: {library_path}")
    else:
        library_path = args.library_path
    
    # Verify paths exist
    if not Path(args.json_path).exists():
        logger.error(f"JSON file not found: {args.json_path}")
        return
    
    if not Path(library_path).exists():
        logger.error(f"Library directory not found: {library_path}")
        return
    
    # Run the sync
    sync_json_with_library(args.json_path, library_path)


if __name__ == "__main__":
    main()
