import re
import json

def extract_quran_to_json(text):
    """
    Extract Quran verses from formatted text and convert to JSON.
    
    Pattern explanation:
    - Chapter header: "NUMBER - Surah NAME (TRANSLATION) [Verses COUNT]"
    - Verses: "Text ending with (VERSE_NUMBER)"
    
    Returns:
        JSON string with structured Quran data
    """
    
    # Split text into chapters based on the pattern
    chapter_pattern = r'(\d+)\s*-\s*Surah\s+([^\(]+)\s*\(([^\)]+)\)\s*\[Verses\s+(\d+)\]'
    
    # Find all chapter headers with their positions
    chapters = []
    for match in re.finditer(chapter_pattern, text):
        chapter_num = int(match.group(1))
        chapter_name = match.group(2).strip()
        verse_count = int(match.group(4))
        chapters.append({
            'number': chapter_num,
            'name': chapter_name,
            'verse_count': verse_count,
            'start_pos': match.end()
        })
    
    # Add end position for each chapter (start of next chapter)
    for i in range(len(chapters) - 1):
        chapters[i]['end_pos'] = chapters[i + 1]['start_pos']
    if chapters:
        chapters[-1]['end_pos'] = len(text)
    
    # Extract verses for each chapter
    result = {}
    
    for chapter in chapters:
        chapter_text = text[chapter['start_pos']:chapter['end_pos']]
        
        # Pattern to match verses ending with (number)
        # This captures text followed by a number in parentheses
        verse_pattern = r'(.+?)\s*\((\d+)\)'
        
        verses = []
        for verse_match in re.finditer(verse_pattern, chapter_text):
            verse_text = verse_match.group(1).strip()
            verse_num = int(verse_match.group(2))
            
            # Clean up the verse text
            # Remove extra whitespace and newlines
            verse_text = ' '.join(verse_text.split())
            
            # Skip empty verses
            if verse_text:
                verses.append({
                    'verse_number': verse_num,
                    'english_text': verse_text
                })
        
        if verses:
            # Create key as "chapter_number:chapter_name:verse_count"
            chapter_key = f"{chapter['number']}:{chapter['name']}:{chapter['verse_count']}"
            result[chapter_key] = {
                'chapter_number': chapter['number'],
                'chapter_name': chapter['name'],
                'total_verses': chapter['verse_count'],
                'verses': verses
            }
    
    return json.dumps(result, indent=2, ensure_ascii=False)


# To use with your full text file:
with open('Holy_Quran_Hashemi_9_Oct_25_Final.txt', 'r', encoding='utf-8') as f:
    quran_text = f.read()
    json_output = extract_quran_to_json(quran_text)
    
    # Save to file
    with open('quran_verses.json', 'w', encoding='utf-8') as out:
        out.write(json_output)
    
    print("JSON file created successfully!")

# Demo with sample
# json_output = extract_quran_to_json(sample_text)
# print(json_output)


def validate_quran_extraction(json_data):
    """
    Validate the extracted Quran data by checking if the number of verses
    matches the expected count in the chapter header.
    
    Args:
        json_data: JSON string or dict containing the extracted Quran data
    
    Returns:
        Dictionary with validation results
    """
    # Parse JSON if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    validation_results = {
        'total_chapters': len(data),
        'valid_chapters': [],
        'invalid_chapters': [],
        'all_valid': True
    }
    
    for chapter_key, chapter_data in data.items():
        # Extract expected count from key (format: "number:name:count")
        key_parts = chapter_key.split(':')
        expected_verses = int(key_parts[2])
        
        # Count actual verses extracted
        actual_verses = len(chapter_data['verses'])
        
        # Also check the total_verses field matches the key
        total_verses_field = chapter_data['total_verses']
        
        # Check for verse number continuity
        verse_numbers = [v['verse_number'] for v in chapter_data['verses']]
        continuity_issues = []
        missing_verses = []
        duplicate_verses = []
        
        # Check for duplicates
        seen = set()
        for vnum in verse_numbers:
            if vnum in seen:
                duplicate_verses.append(vnum)
            seen.add(vnum)
        
        # Check for missing verses (should be 1, 2, 3, ... expected_verses)
        expected_sequence = set(range(1, expected_verses + 1))
        actual_sequence = set(verse_numbers)
        missing_verses = sorted(expected_sequence - actual_sequence)
        extra_verses = sorted(actual_sequence - expected_sequence)
        
        # Check continuity (gaps in sequence)
        if verse_numbers:
            sorted_verses = sorted(verse_numbers)
            for i in range(len(sorted_verses) - 1):
                if sorted_verses[i+1] - sorted_verses[i] > 1:
                    gap_start = sorted_verses[i]
                    gap_end = sorted_verses[i+1]
                    continuity_issues.append(f"Gap between verse {gap_start} and {gap_end}")
        
        # Determine root cause
        root_cause = []
        if missing_verses:
            root_cause.append(f"Missing verses: {missing_verses}")
        if duplicate_verses:
            root_cause.append(f"Duplicate verses: {duplicate_verses}")
        if extra_verses:
            root_cause.append(f"Extra verses (beyond expected): {extra_verses}")
        if continuity_issues:
            root_cause.extend(continuity_issues)
        
        if actual_verses == expected_verses == total_verses_field and not root_cause:
            validation_results['valid_chapters'].append({
                'key': chapter_key,
                'chapter_number': chapter_data['chapter_number'],
                'chapter_name': chapter_data['chapter_name'],
                'verse_count': actual_verses,
                'verse_numbers': verse_numbers,
                'status': 'VALID ✓'
            })
        else:
            validation_results['all_valid'] = False
            validation_results['invalid_chapters'].append({
                'key': chapter_key,
                'chapter_number': chapter_data['chapter_number'],
                'chapter_name': chapter_data['chapter_name'],
                'expected_verses': expected_verses,
                'actual_verses': actual_verses,
                'total_verses_field': total_verses_field,
                'difference': actual_verses - expected_verses,
                'verse_numbers': verse_numbers,
                'missing_verses': missing_verses,
                'duplicate_verses': duplicate_verses,
                'extra_verses': extra_verses,
                'root_cause': root_cause if root_cause else ['Count mismatch but no continuity issues detected'],
                'status': 'MISMATCH ✗'
            })
    validation_results["num_valid"] = len(validation_results.get("valid_chapters"))
    validation_results["num_invalid"] = len(validation_results.get("invalid_chapters"))
    return validation_results


def print_validation_report(validation_results):
    """Print a formatted validation report."""
    print("\n" + "="*80)
    print("QURAN EXTRACTION VALIDATION REPORT")
    print("="*80)
    print(f"\nTotal Chapters: {validation_results['total_chapters']}")
    print(f"Valid Chapters: {len(validation_results['valid_chapters'])}")
    print(f"Invalid Chapters: {len(validation_results['invalid_chapters'])}")
    print(f"\nOverall Status: {'ALL VALID ✓' if validation_results['all_valid'] else 'ERRORS FOUND ✗'}")
    
    if validation_results['invalid_chapters']:
        print("\n" + "-"*80)
        print("CHAPTERS WITH MISMATCHES:")
        print("-"*80)
        for item in validation_results['invalid_chapters']:
            print(f"\n⚠ Chapter {item['chapter_number']}: {item['chapter_name']}")
            print(f"   Key: {item['key']}")
            print(f"   Expected Verses: {item['expected_verses']}")
            print(f"   Actual Verses:   {item['actual_verses']}")
            print(f"   Difference:      {item['difference']:+d}")
            print(f"   Extracted Verse Numbers: {item['verse_numbers'][:10]}{'...' if len(item['verse_numbers']) > 10 else ''}")
            
            # Print root cause analysis
            print(f"\n   ROOT CAUSE ANALYSIS:")
            for cause in item['root_cause']:
                print(f"   • {cause}")
    else:
        print("\n✓ All chapters have the correct number of verses!")
        print("✓ All verse numbers are in proper sequence!")
    
    print("\n" + "="*80)


# Example usage for validation:
validation_results = validate_quran_extraction(json_output)
# print_validation_report(validation_results)
#
# Or save validation report to file:
with open('validation_report.json', 'w', encoding='utf-8') as f:
    json.dump(validation_results, f, indent=2, ensure_ascii=False)