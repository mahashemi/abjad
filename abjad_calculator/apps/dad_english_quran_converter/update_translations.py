#!/usr/bin/env python3
"""
Script to update translation fields in quran_library from translated_chapters.

Only updates if:
1. Arabic text matches (same verse)
2. english_text, urdu_text, persian_text, or transliteration differ

Skips if all translation fields already match.

Usage:
    python update_translations.py           # Run actual update
    python update_translations.py --dry-run # Preview changes without modifying files
"""

import os
import sys
import re
import importlib.util
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Directories
TRANSLATED_DIR = Path(__file__).parent / "translated_chapters"
LIBRARY_DIR = Path(__file__).parent.parent.parent / "quran_library"
LOG_FILE = Path(__file__).parent / "translation_update.log"

# Global flag for dry-run mode
DRY_RUN = False

# Thresholds for updating translations
MIN_EDIT_DISTANCE = 7  # Only update if edit distance > 7 (filters trivial changes)

# Global statistics tracking
TRANSLATION_STATS = {
    'english_text': [],
    'urdu_text': [],
    'persian_text': [],
    'transliteration': []
}

# Track skipped changes due to thresholds
SKIPPED_STATS = {
    'english_text': [],
    'urdu_text': [],
    'persian_text': [],
    'transliteration': []
}

# Verse-level tracking
VERSE_STATS = {
    'total_verses_checked': 0,
    'verses_with_changes': 0,
    'verses_updated': 0,
    'verses_skipped_threshold': 0,
    'verses_unchanged': 0
}


def log_message(message: str, print_to_console: bool = True):
    """Log message to file and optionally print to console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    
    if not DRY_RUN:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    
    if print_to_console:
        print(log_line)


def load_chapter_module(file_path: Path) -> List[Dict]:
    """Load a chapter Python file and extract the ayats list."""
    spec = importlib.util.spec_from_file_location("chapter", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ayats


def extract_header(file_path: Path) -> str:
    """Extract the header docstring from a chapter file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match the opening docstring
    match = re.match(r'("""[\s\S]*?""")', content)
    if match:
        return match.group(1)
    return ""


def normalize_verse_number(verse_num) -> int:
    """Normalize verse number to integer."""
    if isinstance(verse_num, str):
        return int(verse_num)
    return verse_num


def normalize_arabic_text(text: str) -> str:
    """
    Normalize Arabic/Urdu/Persian text to handle Unicode font variations.
    
    Handles common issues:
    - Different Unicode representations of visually identical characters
    - Arabic vs Urdu/Persian character variants
    - Zero-width characters
    - Diacritical marks normalization
    """
    if not text:
        return text
    
    # NFKC normalization: canonical decomposition + composition
    # Handles combining marks and compatibility characters
    normalized = unicodedata.normalize('NFKC', text)
    
    # Character substitutions for Arabic/Urdu/Persian variants
    # These are visually identical but have different Unicode codepoints
    char_map = {
        # Arabic HEH (U+0647) -> Urdu HEH GOAL (U+06C1)
        '\u0647': '\u06C1',  # ه -> ہ
        
        # Arabic YEH variants -> Urdu YEH with hamza
        '\u064A': '\u06CC',  # ي (Arabic) -> ی (Persian/Urdu)
        '\u0649': '\u06CC',  # ى (Alef maksura) -> ی
        
        # Arabic KAF (U+0643) -> Persian/Urdu KEHEH (U+06A9)
        '\u0643': '\u06A9',  # ك (Arabic) -> ک (Persian/Urdu)
        
        # Waw variants
        '\u0624': '\u0624',  # ؤ (normalize to itself)
        
        # Zero-width characters (remove them)
        '\u200C': '',  # Zero-width non-joiner (ZWNJ)
        '\u200D': '',  # Zero-width joiner (ZWJ)
        '\u200B': '',  # Zero-width space
        '\u200E': '',  # Left-to-right mark
        '\u200F': '',  # Right-to-left mark
        '\uFEFF': '',  # Zero-width no-break space (BOM)
        
        # Tatweel (Arabic elongation)
        '\u0640': '',  # ـ (remove tatweel for comparison)
    }
    
    for old_char, new_char in char_map.items():
        normalized = normalized.replace(old_char, new_char)
    
    # Remove combining diacritical marks for comparison (optional - makes comparison more lenient)
    # Uncomment if you want to ignore diacritics completely
    # normalized = ''.join(char for char in normalized 
    #                     if unicodedata.category(char) != 'Mn')
    
    # Normalize whitespace: collapse multiple spaces to single space
    normalized = ' '.join(normalized.split())
    
    return normalized


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance (edit distance) between two strings.
    Returns the minimum number of single-character edits (insertions, deletions, substitutions)
    required to change s1 into s2.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def build_verse_lookup(ayats: List[Dict]) -> Dict[int, Dict]:
    """Build a lookup dictionary mapping verse_number to verse data."""
    lookup = {}
    for ayat in ayats:
        verse_num = normalize_verse_number(ayat.get('verse_number'))
        lookup[verse_num] = ayat
    return lookup


def compare_verses(source_verse: Dict, dest_verse: Dict) -> Tuple[bool, List[str], Dict]:
    """
    Compare two verses and return (needs_update, list_of_differences, updated_fields).
    
    Returns:
        (True, differences, updated_fields) if Arabic matches but translations differ
        (False, [], {}) if all fields match or Arabic doesn't match
    """
    # Check if Arabic text matches
    source_arabic = source_verse.get('arabic_text', '')
    dest_arabic = dest_verse.get('arabic_text', '')
    
    if source_arabic != dest_arabic:
        return False, ["Arabic text mismatch - skipping"], {}
    
    # Check translation fields
    differences = []
    updated_fields = {}
    fields_to_check = ['english_text', 'urdu_text', 'persian_text', 'transliteration']
    
    for field in fields_to_check:
        source_val = source_verse.get(field, '')
        dest_val = dest_verse.get(field, '')
        
        # Apply normalization for RTL languages to handle font variations
        if field in ['urdu_text', 'persian_text', 'transliteration']:
            source_normalized = normalize_arabic_text(source_val)
            dest_normalized = normalize_arabic_text(dest_val)
        else:
            # For English, just normalize whitespace
            source_normalized = ' '.join(source_val.split())
            dest_normalized = ' '.join(dest_val.split())
        
        if source_normalized != dest_normalized:
            # Calculate edit distance on normalized text
            edit_dist = levenshtein_distance(dest_normalized, source_normalized)
            length_diff = abs(len(source_normalized) - len(dest_normalized))
            
            # Check if change meets threshold requirements
            # Only check edit distance (allows same-length rewording)
            meets_threshold = edit_dist > MIN_EDIT_DISTANCE
            
            if meets_threshold:
                differences.append(field)
                
                # Track statistics globally
                TRANSLATION_STATS[field].append({
                    'old_len': len(dest_val),
                    'new_len': len(source_val),
                    'length_diff': length_diff,
                    'edit_distance': edit_dist
                })
                
                updated_fields[field] = {
                    'old': dest_val[:100] + '...' if len(dest_val) > 100 else dest_val,
                    'new': source_val[:100] + '...' if len(source_val) > 100 else source_val,
                    'old_len': len(dest_val),
                    'new_len': len(source_val),
                    'length_diff': length_diff,
                    'edit_distance': edit_dist
                }
            else:
                # Track skipped changes
                SKIPPED_STATS[field].append({
                    'length_diff': length_diff,
                    'edit_distance': edit_dist,
                    'reason': f'Below threshold (len_diff={length_diff}, edit_dist={edit_dist})'
                })
    
    return len(differences) > 0, differences, updated_fields


def format_ayat_entry(ayat: Dict, indent: str = "  ") -> str:
    """Format a single ayat dictionary as Python code."""
    lines = [f"{indent}{{"]
    
    # Add fields in specific order
    fields_order = ['verse_number', 'english_text', 'arabic_text', 'urdu_text', 
                   'persian_text', 'transliteration']
    
    for field in fields_order:
        if field in ayat:
            value = ayat[field]
            if isinstance(value, str):
                # Escape quotes and format string
                value_escaped = value.replace('\\', '\\\\').replace('"', '\\"')
                lines.append(f'{indent}  "{field}": "{value_escaped}",')
            else:
                lines.append(f'{indent}  "{field}": {value},')
    
    lines.append(f"{indent}}},")
    return '\n'.join(lines)


def update_chapter(chapter_num: int, source_file: Path, dest_file: Path, dry_run: bool = False) -> Tuple[bool, int, int, int]:
    """
    Update a chapter file with new translations.
    
    Returns (chapter_updated, verses_checked, verses_updated, verses_skipped_threshold)
    """
    log_message(f"\n{'='*80}")
    log_message(f"Processing Chapter {chapter_num:03d}: {source_file.name}")
    
    # Load both files
    try:
        source_ayats = load_chapter_module(source_file)
        dest_ayats = load_chapter_module(dest_file)
    except Exception as e:
        log_message(f"  ERROR: Failed to load chapter files: {e}")
        return False
    
    # Build lookup dictionaries by verse number
    source_lookup = build_verse_lookup(source_ayats)
    dest_lookup = build_verse_lookup(dest_ayats)
    
    # Get all verse numbers from destination (this is our source of truth)
    dest_verse_numbers = sorted(dest_lookup.keys())
    
    log_message(f"  Source verses: {len(source_lookup)}, Destination verses: {len(dest_lookup)}")
    
    # Check for missing verses in source
    missing_in_source = set(dest_verse_numbers) - set(source_lookup.keys())
    if missing_in_source:
        log_message(f"  WARNING: Verses missing in source: {sorted(missing_in_source)}")
    
    # Compare verses and track changes
    chapter_updated = False
    updated_ayats = []
    verses_checked = 0
    verses_updated = 0
    verses_skipped_threshold = 0
    
    for verse_num in dest_verse_numbers:
        verses_checked += 1
        VERSE_STATS['total_verses_checked'] += 1
        dest_verse = dest_lookup[verse_num]
        
        # Ensure verse_number is stored as int
        dest_verse['verse_number'] = verse_num
        
        if verse_num not in source_lookup:
            log_message(f"  Verse {verse_num}: Not found in source, keeping original")
            updated_ayats.append(dest_verse)
            VERSE_STATS['verses_unchanged'] += 1
            continue
        
        source_verse = source_lookup[verse_num]
        needs_update, differences, updated_fields = compare_verses(source_verse, dest_verse)
        
        # Check if verse had any differences (even if below threshold)
        had_differences = len(differences) > 0 or len(SKIPPED_STATS['english_text']) > 0 or \
                         len(SKIPPED_STATS['urdu_text']) > 0 or len(SKIPPED_STATS['persian_text']) > 0 or \
                         len(SKIPPED_STATS['transliteration']) > 0
        
        if had_differences:
            VERSE_STATS['verses_with_changes'] += 1
        
        if needs_update:
            chapter_updated = True
            verses_updated += 1
            VERSE_STATS['verses_updated'] += 1
            log_message(f"  Verse {verse_num}: Needs update - {', '.join(differences)}")
            
            if dry_run:
                # Show preview of changes
                for field, changes in updated_fields.items():
                    log_message(f"    {field}:")
                    log_message(f"      OLD ({changes['old_len']} chars): {changes['old']}")
                    log_message(f"      NEW ({changes['new_len']} chars): {changes['new']}")
                    log_message(f"      LENGTH DIFFERENCE: {changes['length_diff']} chars")
                    log_message(f"      EDIT DISTANCE: {changes['edit_distance']} operations")
            
            # Create updated verse with new translations
            updated_verse = dest_verse.copy()
            for field in ['english_text', 'urdu_text', 'persian_text', 'transliteration']:
                if field in source_verse:
                    updated_verse[field] = source_verse[field]
            
            updated_ayats.append(updated_verse)
        else:
            # Check if this verse was skipped due to threshold
            verse_had_skips = False
            for field_stats in SKIPPED_STATS.values():
                if len(field_stats) > 0:
                    verse_had_skips = True
                    break
            
            if verse_had_skips and not needs_update:
                verses_skipped_threshold += 1
                VERSE_STATS['verses_skipped_threshold'] += 1
            elif not verse_had_skips:
                VERSE_STATS['verses_unchanged'] += 1
            
            updated_ayats.append(dest_verse)
    
    if not chapter_updated:
        log_message(f"  No updates needed - all translations already match or below threshold")
        return False, verses_checked, verses_updated, verses_skipped_threshold
    
    if dry_run:
        log_message(f"  [DRY RUN] Would update chapter {chapter_num:03d}: {verses_updated} verses")
        return True, verses_checked, verses_updated, verses_skipped_threshold
    
    # Write updated file
    try:
        header = extract_header(dest_file)
        
        with open(dest_file, 'w', encoding='utf-8') as f:
            # Write header
            if header:
                f.write(header + '\n\n')
            
            # Write ayats list
            f.write('ayats = [\n')
            for ayat in updated_ayats:
                f.write(format_ayat_entry(ayat) + '\n')
            f.write(']\n')
        
        log_message(f"  ✓ Successfully updated chapter {chapter_num:03d}: {verses_updated} verses")
        return True, verses_checked, verses_updated, verses_skipped_threshold
        
    except Exception as e:
        log_message(f"  ERROR: Failed to write updated file: {e}")
        return False, verses_checked, 0, verses_skipped_threshold


def find_matching_chapters() -> List[Tuple[int, Path, Path]]:
    """
    Find all matching chapter files between translated_chapters and quran_library.
    
    Returns list of (chapter_number, source_path, dest_path) tuples.
    """
    matches = []
    
    # Get all translated chapter files
    for source_file in sorted(TRANSLATED_DIR.glob("chapter_*.py")):
        # Extract chapter number
        match = re.match(r'chapter_(\d+)_.*\.py', source_file.name)
        if not match:
            continue
        
        chapter_num = int(match.group(1))
        
        # Find corresponding file in quran_library
        dest_files = list(LIBRARY_DIR.glob(f"chapter_{chapter_num:03d}_*.py"))
        
        if len(dest_files) == 1:
            matches.append((chapter_num, source_file, dest_files[0]))
        elif len(dest_files) == 0:
            log_message(f"WARNING: No matching destination file for {source_file.name}", False)
        else:
            log_message(f"WARNING: Multiple destination files for chapter {chapter_num}", False)
    
    return matches


def main():
    """Main execution function."""
    global DRY_RUN
    
    # Check for dry-run flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--dry-run', '-d', '--preview', '-p']:
        DRY_RUN = True
        print("=" * 80)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 80)
        print()
    
    # Initialize log file (only in non-dry-run mode)
    if not DRY_RUN:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"Translation Update Log\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
    
    mode_str = "[DRY RUN] " if DRY_RUN else ""
    log_message(f"{mode_str}Starting translation update process...")
    log_message(f"Source directory: {TRANSLATED_DIR}")
    log_message(f"Destination directory: {LIBRARY_DIR}")
    
    # Find matching chapters
    matches = find_matching_chapters()
    log_message(f"\nFound {len(matches)} matching chapter pairs")
    
    if not matches:
        log_message("ERROR: No matching chapters found!")
        return 1
    
    # Process each chapter
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for chapter_num, source_file, dest_file in matches:
        try:
            was_updated, _, _, _ = update_chapter(chapter_num, source_file, dest_file, dry_run=DRY_RUN)
            if was_updated:
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            log_message(f"  FATAL ERROR processing chapter {chapter_num}: {e}")
            error_count += 1
    
    # Summary
    log_message(f"\n{'='*80}")
    log_message(f"{mode_str}UPDATE SUMMARY")
    log_message(f"{'='*80}")
    log_message(f"Total chapters processed: {len(matches)}")
    action_verb = "would be updated" if DRY_RUN else "updated"
    log_message(f"Chapters {action_verb}: {updated_count}")
    log_message(f"Chapters skipped (no changes): {skipped_count}")
    log_message(f"Chapters with errors: {error_count}")
    
    # Verse-level statistics
    log_message(f"\n{'='*80}")
    log_message(f"VERSE-LEVEL SUMMARY")
    log_message(f"{'='*80}")
    log_message(f"Total verses checked: {VERSE_STATS['total_verses_checked']}")
    log_message(f"Verses with any differences: {VERSE_STATS['verses_with_changes']}")
    log_message(f"Verses {action_verb}: {VERSE_STATS['verses_updated']}")
    log_message(f"Verses skipped (below threshold): {VERSE_STATS['verses_skipped_threshold']}")
    log_message(f"Verses unchanged (identical): {VERSE_STATS['verses_unchanged']}")
    
    # Translation statistics
    log_message(f"\n{'='*80}")
    log_message(f"TRANSLATION CHANGE STATISTICS")
    log_message(f"{'='*80}")
    log_message(f"Update Threshold: Edit Distance > {MIN_EDIT_DISTANCE} (no length filter)")
    
    for field, stats in TRANSLATION_STATS.items():
        if stats:
            total_changes = len(stats)
            edit_distances = [s['edit_distance'] for s in stats]
            length_diffs = [s['length_diff'] for s in stats]
            
            # Sort for percentile calculations
            sorted_edit_dist = sorted(edit_distances)
            sorted_length_diff = sorted(length_diffs)
            
            # Edit distance statistics
            total_edit_dist = sum(edit_distances)
            avg_edit_dist = total_edit_dist / total_changes
            min_edit = min(edit_distances)
            max_edit = max(edit_distances)
            median_edit = sorted_edit_dist[len(sorted_edit_dist) // 2]
            
            # Percentiles for edit distance
            p25_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.25)]
            p50_edit = median_edit
            p75_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.75)]
            p90_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.90)]
            p95_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.95)]
            p99_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.99)]
            
            # Length difference statistics
            total_length_diff = sum(length_diffs)
            avg_length_diff = total_length_diff / total_changes
            min_len = min(length_diffs)
            max_len = max(length_diffs)
            median_len = sorted_length_diff[len(sorted_length_diff) // 2]
            
            # Mode for edit distance (most common value)
            from collections import Counter
            edit_counts = Counter(edit_distances)
            mode_edit = edit_counts.most_common(1)[0][0]
            mode_edit_count = edit_counts.most_common(1)[0][1]
            
            log_message(f"\n{field}:")
            log_message(f"  Total changes: {total_changes}")
            log_message(f"  Edit Distance (Levenshtein):")
            log_message(f"    Total: {total_edit_dist:,} operations")
            log_message(f"    Mean: {avg_edit_dist:.1f}")
            log_message(f"    Median: {median_edit}")
            log_message(f"    Mode: {mode_edit} (occurs {mode_edit_count} times)")
            log_message(f"    Min/Max: {min_edit} / {max_edit}")
            log_message(f"    Percentiles:")
            log_message(f"      P25: {p25_edit}  |  P50: {p50_edit}  |  P75: {p75_edit}")
            log_message(f"      P90: {p90_edit}  |  P95: {p95_edit}  |  P99: {p99_edit}")
            log_message(f"  String Length Difference:")
            log_message(f"    Total: {total_length_diff:,} characters")
            log_message(f"    Mean: {avg_length_diff:.1f}")
            log_message(f"    Median: {median_len}")
            log_message(f"    Min/Max: {min_len} / {max_len}")
            
            # Distribution buckets for edit distance
            buckets = {
                '0-10': 0,
                '11-50': 0,
                '51-100': 0,
                '101-200': 0,
                '201-500': 0,
                '500+': 0
            }
            
            for s in stats:
                dist = s['edit_distance']
                if dist <= 10:
                    buckets['0-10'] += 1
                elif dist <= 50:
                    buckets['11-50'] += 1
                elif dist <= 100:
                    buckets['51-100'] += 1
                elif dist <= 200:
                    buckets['101-200'] += 1
                elif dist <= 500:
                    buckets['201-500'] += 1
                else:
                    buckets['500+'] += 1
            
            log_message(f"  Edit Distance Distribution:")
            for bucket, count in buckets.items():
                percentage = (count / total_changes * 100) if total_changes > 0 else 0
                log_message(f"    {bucket:>10} edits: {count:4} ({percentage:5.1f}%)")
    
    # Skipped changes statistics
    total_skipped = sum(len(stats) for stats in SKIPPED_STATS.values())
    if total_skipped > 0:
        log_message(f"\n{'='*80}")
        log_message(f"SKIPPED CHANGES (Below Threshold)")
        log_message(f"{'='*80}")
        for field, skipped in SKIPPED_STATS.items():
            if skipped:
                edit_distances = [s['edit_distance'] for s in skipped]
                length_diffs = [s['length_diff'] for s in skipped]
                
                sorted_edit_dist = sorted(edit_distances)
                sorted_length_diff = sorted(length_diffs)
                
                # Edit distance stats
                avg_edit_dist = sum(edit_distances) / len(edit_distances)
                min_edit = min(edit_distances)
                max_edit = max(edit_distances)
                median_edit = sorted_edit_dist[len(sorted_edit_dist) // 2]
                
                # Percentiles
                p25_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.25)]
                p75_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.75)]
                p90_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.90)]
                p95_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.95)]
                p99_edit = sorted_edit_dist[int(len(sorted_edit_dist) * 0.99)] if len(sorted_edit_dist) > 100 else max_edit
                
                # Length diff stats
                avg_len_diff = sum(length_diffs) / len(length_diffs)
                median_len = sorted_length_diff[len(sorted_length_diff) // 2]
                
                from collections import Counter
                edit_counts = Counter(edit_distances)
                mode_edit = edit_counts.most_common(1)[0][0]
                
                log_message(f"\n{field}:")
                log_message(f"  Total skipped: {len(skipped)}")
                log_message(f"  Edit Distance:")
                log_message(f"    Mean: {avg_edit_dist:.1f}")
                log_message(f"    Median: {median_edit}")
                log_message(f"    Mode: {mode_edit}")
                log_message(f"    Min/Max: {min_edit} / {max_edit}")
                log_message(f"    Percentiles: P25={p25_edit} | P75={p75_edit} | P90={p90_edit} | P95={p95_edit} | P99={p99_edit}")
                log_message(f"  Length Difference:")
                log_message(f"    Mean: {avg_len_diff:.1f}")
                log_message(f"    Median: {median_len}")
    
    # Threshold recommendations
    log_message(f"\n{'='*80}")
    log_message(f"THRESHOLD ANALYSIS & RECOMMENDATIONS")
    log_message(f"{'='*80}")
    log_message(f"Current threshold: Edit Distance > {MIN_EDIT_DISTANCE}")
    log_message(f"")
    log_message(f"This threshold:")
    log_message(f"  • Filters trivial changes (1-{MIN_EDIT_DISTANCE} character differences)")
    log_message(f"  • Captures meaningful rewording regardless of length change")
    log_message(f"  • Includes same-length text changes (important translations)")
    
    if not DRY_RUN:
        log_message(f"\nLog file saved to: {LOG_FILE}")
    else:
        log_message(f"\nTo apply these changes, run without --dry-run flag")
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
