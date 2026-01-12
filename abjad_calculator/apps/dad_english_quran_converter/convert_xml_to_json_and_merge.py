import json
import xml.etree.ElementTree as ET


def parse_arabic_xml(xml_file_path):
    """
    Parse the Arabic Quran XML file.
    
    Args:
        xml_file_path: Path to the XML file
    
    Returns:
        Dictionary with structure: {sura_index: {aya_index: arabic_text}}
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    arabic_data = {}
    
    for sura in root.findall('sura'):
        sura_index = int(sura.get('index'))
        sura_name = sura.get('name')
        
        arabic_data[sura_index] = {
            'name': sura_name,
            'ayas': {}
        }
        
        for aya in sura.findall('aya'):
            aya_index = int(aya.get('index'))
            aya_text = aya.get('text')
            
            arabic_data[sura_index]['ayas'][aya_index] = aya_text
    
    return arabic_data


def merge_arabic_with_english(english_json_path, arabic_xml_path):
    """
    Merge Arabic text from XML with English JSON.
    
    Args:
        english_json_path: Path to the English JSON file
        arabic_xml_path: Path to the Arabic XML file
    
    Returns:
        Merged dictionary with both Arabic and English
    """
    # Load English JSON
    with open(english_json_path, 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    # Parse Arabic XML
    arabic_data = parse_arabic_xml(arabic_xml_path)
    
    # Merge data
    merged_data = {}
    
    for chapter_key, chapter_data in english_data.items():
        chapter_number = chapter_data['chapter_number']
        
        # Check if Arabic data exists for this chapter
        if chapter_number not in arabic_data:
            print(f"⚠ Warning: No Arabic data found for chapter {chapter_number}")
            continue
        
        # Create new merged chapter
        merged_chapter = {
            'chapter_number': chapter_data['chapter_number'],
            'chapter_name': chapter_data['chapter_name'],
            'chapter_name_arabic': arabic_data[chapter_number]['name'],
            'total_verses': chapter_data['total_verses'],
            'verses': []
        }
        
        # Merge verses
        for verse in chapter_data['verses']:
            verse_number = verse['verse_number']
            
            merged_verse = {
                'verse_number': verse_number,
                'english_text': verse['english_text'],
                'arabic_text': arabic_data[chapter_number]['ayas'].get(verse_number, '')
            }
            
            merged_chapter['verses'].append(merged_verse)
        
        merged_data[chapter_key] = merged_chapter
    
    return merged_data


def validate_merge(merged_data, arabic_data):
    """
    Validate that the merge was successful by checking verse counts.
    
    Args:
        merged_data: The merged dictionary
        arabic_data: The parsed Arabic data
    
    Returns:
        Validation results dictionary
    """
    validation_results = {
        'total_chapters': len(merged_data),
        'valid_chapters': [],
        'invalid_chapters': [],
        'all_valid': True
    }
    
    for chapter_key, chapter_data in merged_data.items():
        chapter_number = chapter_data['chapter_number']
        chapter_name = chapter_data['chapter_name']
        
        # Count verses in merged data
        english_verse_count = len(chapter_data['verses'])
        
        # Count ayas in Arabic data
        arabic_aya_count = len(arabic_data.get(chapter_number, {}).get('ayas', {}))
        
        # Check for missing Arabic text
        missing_arabic = []
        for verse in chapter_data['verses']:
            if not verse.get('arabic_text'):
                missing_arabic.append(verse['verse_number'])
        
        # Validate
        if english_verse_count == arabic_aya_count and not missing_arabic:
            validation_results['valid_chapters'].append({
                'chapter_number': chapter_number,
                'chapter_name': chapter_name,
                'verse_count': english_verse_count,
                'status': 'VALID ✓'
            })
        else:
            validation_results['all_valid'] = False
            
            root_cause = []
            if english_verse_count != arabic_aya_count:
                root_cause.append(f"Verse count mismatch: English={english_verse_count}, Arabic={arabic_aya_count}")
            if missing_arabic:
                root_cause.append(f"Missing Arabic text for verses: {missing_arabic}")
            
            validation_results['invalid_chapters'].append({
                'chapter_number': chapter_number,
                'chapter_name': chapter_name,
                'english_verse_count': english_verse_count,
                'arabic_aya_count': arabic_aya_count,
                'missing_arabic_verses': missing_arabic,
                'root_cause': root_cause,
                'status': 'MISMATCH ✗'
            })
    
    return validation_results


def print_merge_validation_report(validation_results):
    """Print a formatted validation report for the merge."""
    print("\n" + "="*80)
    print("ARABIC-ENGLISH MERGE VALIDATION REPORT")
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
            print(f"   English Verse Count: {item['english_verse_count']}")
            print(f"   Arabic Aya Count:    {item['arabic_aya_count']}")
            if item['missing_arabic_verses']:
                print(f"   Missing Arabic Text: {item['missing_arabic_verses']}")
            
            print(f"\n   ROOT CAUSE ANALYSIS:")
            for cause in item['root_cause']:
                print(f"   • {cause}")
    else:
        print("\n✓ All chapters have matching verse counts!")
        print("✓ All verses have Arabic text!")
    
    print("\n" + "="*80)


# Example usage:
def main():
    # File paths
    english_json_path = 'quran_verses.json'
    arabic_xml_path = '/Users/mohammadabuzarhashemi/Downloads/hashemi_documents/code_space/workspace/abjad/tests/quran-uthmani.xml'
    output_json_path = 'quran_bilingual.json'
    
    print("Starting Arabic-English merge...")
    
    # Parse Arabic XML first to have it for validation
    print("\n1. Parsing Arabic XML...")
    arabic_data = parse_arabic_xml(arabic_xml_path)
    print(f"   ✓ Parsed {len(arabic_data)} chapters from XML")
    
    # Merge
    print("\n2. Merging Arabic and English...")
    merged_data = merge_arabic_with_english(english_json_path, arabic_xml_path)
    print(f"   ✓ Merged {len(merged_data)} chapters")
    
    # Validate
    print("\n3. Validating merge...")
    validation_results = validate_merge(merged_data, arabic_data)
    print_merge_validation_report(validation_results)
    
    # Save merged data
    if validation_results['all_valid']:
        print(f"\n4. Saving merged data to {output_json_path}...")
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        print("   ✓ File saved successfully!")
    else:
        print("\n⚠ Merge has errors. Please review before saving.")
        save_anyway = input("Save anyway? (yes/no): ")
        if save_anyway.lower() == 'yes':
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, indent=2, ensure_ascii=False)
            print("   ✓ File saved with warnings!")


# Uncomment to run:
main()

# Or use individual functions:
# arabic_data = parse_arabic_xml('quran_arabic.xml')
# merged = merge_arabic_with_english('quran_verses.json', 'quran_arabic.xml')
# validation = validate_merge(merged, arabic_data)
# print_merge_validation_report(validation)