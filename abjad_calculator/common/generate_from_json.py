#!/usr/bin/env python3
"""Script to generate missing surah imports and entries from quran_bilingual.json"""

import json
from pathlib import Path

def main():
    # Read the JSON file
    json_path = Path(__file__).parent.parent / "apps/dad_english_quran_converter/quran_bilingual.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        quran_data = json.load(f)
    
    # Get quran library path
    quran_lib = Path(__file__).parent.parent / "quran_library"
    
    # Get all existing chapter files
    chapter_files = sorted([f for f in quran_lib.glob("chapter_*.py") if f.name != "__init__.py"])
    
    # Extract chapter numbers and names from files
    existing_chapters = {}
    for f in chapter_files:
        parts = f.stem.split('_', 2)  # chapter_XXX_name
        if len(parts) >= 3:
            chapter_num = int(parts[1])
            name_part = '_'.join(parts[2:])
            existing_chapters[chapter_num] = name_part
    
    # Parse JSON data
    surah_info = {}
    for key, value in quran_data.items():
        ch_num = value['chapter_number']
        ch_name_arabic = value['chapter_name_arabic']
        total_verses = value['total_verses']
        surah_info[ch_num] = {
            'arabic': ch_name_arabic,
            'verses': total_verses
        }
    
    print("=" * 80)
    print("IMPORTS TO ADD TO surah_factory.py (sorted by chapter number)")
    print("=" * 80)
    print("\nfrom ..quran_library import (")
    
    for ch_num in sorted(existing_chapters.keys()):
        print(f"    chapter_{ch_num:03d}_{existing_chapters[ch_num]},")
    
    print(")")
    
    print("\n" + "=" * 80)
    print("TITLE DEFINITIONS TO ADD")
    print("=" * 80)
    print()
    
    for ch_num in sorted(existing_chapters.keys()):
        if ch_num in surah_info:
            arabic = surah_info[ch_num]['arabic']
            verses = surah_info[ch_num]['verses']
            var_name = existing_chapters[ch_num].replace('-', '_').replace("'", "").replace('[', '').replace(']', '').replace(' ', '_')
            print(f'surah_{var_name}_title = "سورة {arabic} - سورة {ch_num} - عدد آياتها {verses}".strip()')
    
    print("\n" + "=" * 80)
    print("DICTIONARY ENTRIES TO ADD (sorted by chapter number)")
    print("=" * 80)
    print()
    
    for ch_num in sorted(existing_chapters.keys()):
        var_name = existing_chapters[ch_num].replace('-', '_').replace("'", "").replace('[', '').replace(']', '').replace(' ', '_')
        print(f"    surah_{var_name}_title: chapter_{ch_num:03d}_{existing_chapters[ch_num]}.ayats,")
    
    print("\n" + "=" * 80)
    print(f"Total chapters in library: {len(existing_chapters)}")
    print(f"Total chapters in JSON: {len(surah_info)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
