"""
Build comprehensive search index for Quran with all translations and abjad values.
This script consolidates data from quran_library and debug folder into a single JSON
file for static site search functionality.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import from quran_library
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

from abjad_calculator.common.surah_factory import surahs
from abjad_calculator.common.core import calculate_abjad


def load_abjad_values(chapter_num, verse_num, debug_base_path):
    """Load abjad calculation values from debug folder."""
    # Try Arabic folder name format
    debug_path = os.path.join(debug_base_path, f"سورة {chapter_num}", str(verse_num), "result.json")
    
    if os.path.exists(debug_path):
        try:
            with open(debug_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    'qamari': data.get('total_qamari_value', 0),
                    'malfuzi': data.get('total_malfuzi_value', 0),
                    'bayenati': data.get('total_bayenati_value', 0),
                    'letter_counts': data.get('letter_counts', {}),
                    'cleaned_text': data.get('cleaned_text', '')
                }
        except Exception as e:
            print(f"Warning: Could not load abjad values for {chapter_num}:{verse_num} - {e}")
    
    return {'qamari': 0, 'malfuzi': 0, 'bayenati': 0, 'letter_counts': {}, 'cleaned_text': ''}


def compute_word_abjad_stats(arabic_text):
    """Compute word-level abjad statistics from Arabic text."""
    words = [w.strip() for w in arabic_text.split() if w.strip()]
    word_stats = []
    
    for idx, word in enumerate(words, 1):
        try:
            result = calculate_abjad(word)
            word_stats.append({
                'position': idx,
                'word': word,
                'qamari': result.total_qamari_value,
                'malfuzi': result.total_malfuzi_value,
                'bayenati': result.total_bayenati_value
            })
        except Exception as e:
            print(f"Warning: Could not calculate abjad for word '{word}': {e}")
            word_stats.append({
                'position': idx,
                'word': word,
                'qamari': 0,
                'malfuzi': 0,
                'bayenati': 0
            })
    
    return word_stats


def build_search_index(debug_folder_path, output_path):
    """
    Build comprehensive search index from quran_library and debug data.
    
    Args:
        debug_folder_path: Path to debug folder containing abjad calculations
        output_path: Path where to save the output JSON file
    """
    print("Building Quran search index...")
    
    search_data = {
        "metadata": {
            "total_chapters": 114,
            "total_verses": 0,
            "languages": ["arabic", "urdu", "persian", "english", "transliteration"],
            "abjad_systems": ["qamari", "malfuzi", "bayenati"],
            "generated": datetime.now().isoformat(),
            "description": "Complete Quran search index with multi-language support and abjad numerical values"
        },
        "chapters": []
    }
    
    total_verses = 0
    
    # Iterate through all surahs
    for surah_title, verses in surahs.items():
        # Parse surah info from title
        # Format: "سورة الفاتحة - سورة 1 - عدد آياتها 7"
        parts = surah_title.split('-')
        chapter_name_arabic = parts[0].strip().replace('سورة ', '')
        chapter_number = int(parts[1].strip().replace('سورة ', ''))
        verse_count = int(parts[2].strip().replace('عدد آياتها ', '').replace('عدد', '').strip())
        
        chapter_data = {
            "chapter_number": chapter_number,
            "chapter_name_arabic": chapter_name_arabic,
            "total_verses": verse_count,
            "verses": [],
            "chapter_abjad_totals": {
                "qamari": 0,
                "malfuzi": 0,
                "bayenati": 0
            }
        }
        
        # Process each verse
        for verse in verses:
            verse_number = verse.get('verse_number')
            arabic_text = verse.get('arabic_text', '')
            
            # Load abjad values from debug folder
            abjad_data = load_abjad_values(chapter_number, verse_number, debug_folder_path)
            
            # Use cleaned text for word calculations (same as calculator)
            cleaned_text = abjad_data.pop('cleaned_text', arabic_text)
            
            # Compute word-level abjad statistics using cleaned text
            word_stats = compute_word_abjad_stats(cleaned_text)
            
            verse_data = {
                "verse_number": verse_number,
                "arabic": arabic_text,  # Original text with diacritics for display
                "arabic_clean": cleaned_text,  # Cleaned text used for calculations
                "urdu": verse.get('urdu_text', ''),
                "persian": verse.get('persian_text', ''),
                "english": verse.get('english_text', ''),
                "transliteration": verse.get('transliteration', ''),
                "abjad": abjad_data,
                "word_count": len(word_stats),
                "words": word_stats  # Word-level abjad data for future dashboard
            }
            
            chapter_data["verses"].append(verse_data)
            total_verses += 1
            
            # Accumulate chapter totals
            chapter_data["chapter_abjad_totals"]["qamari"] += abjad_data.get("qamari", 0)
            chapter_data["chapter_abjad_totals"]["malfuzi"] += abjad_data.get("malfuzi", 0)
            chapter_data["chapter_abjad_totals"]["bayenati"] += abjad_data.get("bayenati", 0)
        
        search_data["chapters"].append(chapter_data)
        print(f"Processed Chapter {chapter_number}: {chapter_name_arabic} ({verse_count} verses)")
    
    search_data["metadata"]["total_verses"] = total_verses
    
    # Save to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    # Get file size
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"\n✅ Search index built successfully!")
    print(f"   Total verses: {total_verses}")
    print(f"   Output file: {output_path}")
    print(f"   File size: {file_size_mb:.2f} MB")
    
    return search_data


if __name__ == "__main__":
    # Get paths (already defined at top for imports)
    debug_folder = project_root.parent / "debug"
    output_file = project_root / "static" / "data" / "quran_search_index.json"
    
    print(f"Debug folder: {debug_folder}")
    print(f"Output file: {output_file}")
    print()
    
    if not debug_folder.exists():
        print(f"❌ Error: Debug folder not found at {debug_folder}")
        sys.exit(1)
    
    build_search_index(str(debug_folder), str(output_file))