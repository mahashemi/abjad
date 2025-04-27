#!/bin/bash
# Script to set up Abjad Calculator library

echo "Setting up Abjad Calculator library..."

# Create main directory
mkdir -p abjad_calculator

# Create Python files
touch abjad_calculator/__init__.py
touch abjad_calculator/core.py
touch abjad_calculator/display.py
touch abjad_calculator/naqsh.py
touch abjad_calculator/quran.py
touch abjad_calculator/utils.py
touch abjad_calculator/constants.py
touch main.py

# Write content to constants.py
cat > abjad_calculator/constants.py << 'EOL'
"""
Constants and mappings for the Abjad Calculator.
"""

# Standard Abjad value mappings
ABJAD_VALUES = {
    'ا': 1,    'أ': 1,    'إ': 1,    'آ': 1,    # Alif variations
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5,    'ة': 5,    # Ha variations
    'و': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10,   'ى': 10,   'ئ': 10,   # Ya variations
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

# Special characters to remove before processing
REMOVE_CHARS = [
    'ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ', 'ٓ', 'ۚ', '۟', '۠', 'ۡ', 
    'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', '۩', '۪', '۫', '۬', 'ۭ',  # Diacritics
    ' ', '\n', '\t'  # Whitespace
]

# Pre-defined texts for naqsh generation
PRESET_TEXTS = {
    "bastam_dard_sar": "ب س ت م د ر د س ر",
    "bastam_dard_kamar": "ب س ت م د ر د ك م ر",
    "huruf_sawamat": "ا ح د ر س ص ط ع ك ل م و ه",
}
EOL

# Write content to core.py
cat > abjad_calculator/core.py << 'EOL'
"""
Core functions for Abjad calculation.
"""

from .constants import ABJAD_VALUES, REMOVE_CHARS

def clean_text(text):
    """Clean Arabic text by removing diacritics and standardizing characters."""
    # Replace alif wasla with regular alif
    text = text.replace('ٱ', 'ا')
    
    # Remove diacritics and whitespace
    for char in REMOVE_CHARS:
        text = text.replace(char, '')
    
    return text

def calculate_abjad(text):
    """Calculate the Abjad numerical value of Arabic text."""
    original_text = text
    cleaned_text = clean_text(text)
    
    # Initialize result dictionary
    result = {
        'original_text': original_text,
        'cleaned_text': cleaned_text,
        'total_value': 0,
        'breakdown': [],
        'letter_values': [],
        'letter_counts': {}
    }
    
    # Calculate letter by letter
    for char in cleaned_text:
        if char in ABJAD_VALUES:
            value = ABJAD_VALUES[char]
            result['breakdown'].append({'letter': char, 'value': value})
            result['letter_values'].append({char: value})
            result['total_value'] += value
            
            # Count occurrences of each letter
            result['letter_counts'][char] = result['letter_counts'].get(char, 0) + 1
    
    # Add verification data
    result['verification'] = {}
    verification_total = 0
    
    for letter, count in result['letter_counts'].items():
        sub_total = count * ABJAD_VALUES[letter]
        verification_total += sub_total
        result['verification'][letter] = {
            'count': count,
            'value': ABJAD_VALUES[letter],
            'total': sub_total
        }
    
    result['verification_total'] = verification_total
    
    return result

def calculate_special_properties(result):
    """Calculate special properties from the abjad total."""
    total = result['total_value']
    total_minus_12 = total - 12
    
    quotient, remainder = divmod(total_minus_12, 3)
    increment_cell = 2 if remainder == 2 else 7
    
    return {
        'total_minus_12': total_minus_12,
        'division_by_3': {
            'quotient': quotient,
            'remainder': remainder
        },
        'increment_cell': increment_cell
    }
EOL

# Write content to utils.py
cat > abjad_calculator/utils.py << 'EOL'
"""
Utility functions for the Abjad Calculator.
"""

def normalize_space_separated_text(text):
    """Convert space-separated characters to a clean list without empty entries."""
    return [c.strip() for c in text.split() if c.strip()]

def interleave_texts(text1, text2):
    """Interleave two character lists."""
    chars1 = text1 if isinstance(text1, list) else normalize_space_separated_text(text1)
    chars2 = text2 if isinstance(text2, list) else normalize_space_separated_text(text2)
    
    interleaved = []
    for i in range(max(len(chars1), len(chars2))):
        if i < len(chars1):
            interleaved.append(chars1[i])
        if i < len(chars2):
            interleaved.append(chars2[i])
    
    return interleaved

def split_into_groups(text_list, group_size=4):
    """Split a list of characters into groups of specified size."""
    groups = []
    for i in range(0, len(text_list), group_size):
        group = text_list[i:i + group_size]
        groups.append(''.join(group))
    return groups

def format_custom_output(result):
    """Format the calculation result into the custom output format."""
    return str(result['letter_values'][::-1])
EOL

# Write content to display.py
cat > abjad_calculator/display.py << 'EOL'
"""
Display functions for Abjad calculation results.
"""

import pandas as pd
from .constants import ABJAD_VALUES

def create_abjad_dataframe(result):
    """
    Convert abjad calculation result to pandas DataFrames.
    
    Args:
        result (dict): Result from calculate_abjad function
        
    Returns:
        tuple: (letter_df, summary_df) - Two DataFrames with detailed and summary information
    """
    # Create letter-by-letter DataFrame
    letter_data = []
    for item in result['breakdown']:
        letter_data.append({
            'Letter': item['letter'],
            'Abjad Value': item['value']
        })
    
    letter_df = pd.DataFrame(letter_data)
    
    # Create summary DataFrame (for letter counts and totals)
    summary_data = []
    for letter, data in sorted(result['verification'].items(), key=lambda x: ABJAD_VALUES[x[0]]):
        summary_data.append({
            'Letter': letter,
            'Count': data['count'],
            'Abjad Value': data['value'],
            'Subtotal': data['total']
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values(by='Abjad Value')
    
    return letter_df, summary_df

def render_abjad_table_html(result, title=None):
    """
    Render abjad calculation as HTML tables.
    
    Args:
        result (dict): Result from calculate_abjad function
        title (str, optional): Title for the table
        
    Returns:
        str: HTML string with styled tables
    """
    letter_df, summary_df = create_abjad_dataframe(result)
    
    # Style for the tables
    styles = [
        # Table borders and alignment
        {
            'selector': 'table',
            'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('margin-bottom', '20px'),
                ('font-family', 'Arial, sans-serif')
            ]
        },
        # Header styling
        {
            'selector': 'th',
            'props': [
                ('background-color', '#f2f2f2'),
                ('color', '#333'),
                ('font-weight', 'bold'),
                ('text-align', 'center'),
                ('padding', '8px'),
                ('border', '1px solid #ddd')
            ]
        },
        # Cell styling
        {
            'selector': 'td',
            'props': [
                ('padding', '8px'),
                ('border', '1px solid #ddd'),
                ('text-align', 'center')
            ]
        },
        # Alternating row colors
        {
            'selector': 'tbody tr:nth-child(even)',
            'props': [('background-color', '#f9f9f9')]
        }
    ]
    
    # Create title if provided
    title_html = f"<h2 style='text-align:center; font-family:Arial,sans-serif;'>{title}</h2>" if title else ""
    
    # Original text display
    original_text_html = f"""
    <div style="margin-bottom:15px; font-family:Arial,sans-serif;">
        <p><strong>Original Text:</strong> {result['original_text']}</p>
        <p><strong>Cleaned Text:</strong> {result['cleaned_text']}</p>
    </div>
    """
    
    # Create styled DataFrames
    letter_styled = letter_df.style.set_table_styles(styles).set_caption('Letter-by-Letter Breakdown')
    summary_styled = summary_df.style.set_table_styles(styles).set_caption('Summary by Letter')
    
    # Total values section
    totals_html = f"""
    <div style="margin:15px 0; padding:10px; background-color:#f2f2f2; border-radius:5px; font-family:Arial,sans-serif;">
        <p><strong>Total Abjad Value:</strong> {result['total_value']}</p>
        <p><strong>Verification Total:</strong> {result['verification_total']}</p>
    </div>
    """
    
    # Combine all HTML components
    full_html = f"""
    <div style="padding:15px; max-width:800px; margin:0 auto;">
        {title_html}
        {original_text_html}
        <h3 style="font-family:Arial,sans-serif;">Letter-by-Letter Breakdown</h3>
        {letter_styled.to_html()}
        <h3 style="font-family:Arial,sans-serif;">Summary by Letter</h3>
        {summary_styled.to_html()}
        {totals_html}
    </div>
    <hr style="border:0; border-top:1px solid #ddd; margin:30px 0;">
    """
    
    return full_html

def calculate_arabic_text_with_table(text, title=None, output_html=False, output_path=None):
    """
    Calculate abjad value for any Arabic text and display as a table.
    
    Args:
        text (str): Arabic text to calculate
        title (str, optional): Title for the output
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        
    Returns:
        str: HTML string of the table
    """
    from .core import calculate_abjad
    
    result = calculate_abjad(text)
    html_output = render_abjad_table_html(result, title)
    
    # Save to file if requested
    if output_html:
        path = output_path or f"abjad_calculation_{hash(text)}.html"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"HTML output saved to {path}")
    
    # In a Jupyter environment, display the HTML directly
    try:
        from IPython import get_ipython
        from IPython.display import HTML, display
        if get_ipython() is not None:
            display(HTML(html_output))
    except:
        pass
    
    return html_output

def calculate_multiple_texts_with_tables(texts_dict, output_html=False, output_path=None):
    """
    Calculate abjad values for multiple texts and display as tables.
    
    Args:
        texts_dict (dict): Dictionary with text identifiers as keys and texts as values
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        
    Returns:
        str: Combined HTML string of all tables
    """
    from .core import calculate_abjad
    
    all_html = ""
    grand_total = 0
    
    for text_id, text in texts_dict.items():
        result = calculate_abjad(text)
        grand_total += result['total_value']
        html = render_abjad_table_html(result, f"Text {text_id}")
        all_html += html
    
    # Add grand total section
    grand_total_html = f"""
    <div style="margin:20px 0; padding:15px; background-color:#e8f4f8; border-radius:5px; font-family:Arial,sans-serif; text-align:center;">
        <h2>Grand Total for All Texts: {grand_total}</h2>
    </div>
    """
    
    all_html = f"""
    <div style="padding:20px; font-family:Arial,sans-serif;">
        <h1 style="text-align:center;">Abjad Calculation Results</h1>
        {all_html}
        {grand_total_html}
    </div>
    """
    
    # Save to file if requested
    if output_html:
        path = output_path or f"multiple_abjad_calculations.html"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(all_html)
        print(f"HTML output saved to {path}")
    
    # In a Jupyter environment, display the HTML directly
    try:
        from IPython import get_ipython
        from IPython.display import HTML, display
        if get_ipython() is not None:
            display(HTML(all_html))
    except:
        pass
    
    return all_html
EOL

# Write content to naqsh.py
cat > abjad_calculator/naqsh.py << 'EOL'
"""
Functions for Naqsh generation and calculation.
"""

from .constants import PRESET_TEXTS
from .core import calculate_abjad
from .utils import normalize_space_separated_text, interleave_texts, split_into_groups

def generate_naqsh_dard_sar(name_with_mothers_name, custom_sawamat=None):
    """
    Generate a Naqsh for pain relief (head) using name and huruf sawamat.
    
    Args:
        name_with_mothers_name (str): Name and mother's name in space-separated Arabic letters
        custom_sawamat (str, optional): Custom huruf sawamat. If None, defaults to preset.
        
    Returns:
        dict: Complete naqsh calculation results
    """
    # Use default or custom huruf sawamat
    huruf_sawamat = custom_sawamat if custom_sawamat else PRESET_TEXTS["huruf_sawamat"]
    bastam_text = PRESET_TEXTS["bastam_dard_sar"]
    
    # Process the texts
    name_chars = normalize_space_separated_text(name_with_mothers_name)
    sawamat_chars = normalize_space_separated_text(huruf_sawamat)
    bastam_chars = normalize_space_separated_text(bastam_text)
    
    # Combine bastam with name
    combined_text = bastam_chars + name_chars
    
    # Interleave huruf sawamat with combined text
    interleaved_chars = interleave_texts(sawamat_chars, combined_text)
    interleaved_text = ' '.join(interleaved_chars)
    
    # Calculate abjad value
    result = calculate_abjad(interleaved_text)
    
    # Add some additional information to the result
    result['naqsh_type'] = 'dard_sar'
    result['huruf_sawamat'] = huruf_sawamat
    result['bastam_text'] = bastam_text
    result['name_with_mothers_name'] = name_with_mothers_name
    result['interleaved_text'] = interleaved_text
    
    # Create groups of 4 for the naqsh squares
    grouped_chars = split_into_groups(interleaved_chars)
    result['naqsh_squares'] = grouped_chars
    
    return result

def generate_naqsh_dard_kamar(name_with_mothers_name, custom_sawamat=None):
    """
    Generate a Naqsh for pain relief (back) using name and huruf sawamat.
    
    Args:
        name_with_mothers_name (str): Name and mother's name in space-separated Arabic letters
        custom_sawamat (str, optional): Custom huruf sawamat. If None, defaults to preset.
        
    Returns:
        dict: Complete naqsh calculation results
    """
    # Use default or custom huruf sawamat
    huruf_sawamat = custom_sawamat if custom_sawamat else PRESET_TEXTS["huruf_sawamat"]
    bastam_text = PRESET_TEXTS["bastam_dard_kamar"]
    
    # Process the texts
    name_chars = normalize_space_separated_text(name_with_mothers_name)
    sawamat_chars = normalize_space_separated_text(huruf_sawamat)
    bastam_chars = normalize_space_separated_text(bastam_text)
    
    # Combine bastam with name
    combined_text = bastam_chars + name_chars
    
    # Interleave huruf sawamat with combined text
    interleaved_chars = interleave_texts(sawamat_chars, combined_text)
    interleaved_text = ' '.join(interleaved_chars)
    
    # Calculate abjad value
    result = calculate_abjad(interleaved_text)
    
    # Add some additional information to the result
    result['naqsh_type'] = 'dard_kamar'
    result['huruf_sawamat'] = huruf_sawamat
    result['bastam_text'] = bastam_text
    result['name_with_mothers_name'] = name_with_mothers_name
    result['interleaved_text'] = interleaved_text
    
    # Create groups of 4 for the naqsh squares
    grouped_chars = split_into_groups(interleaved_chars)
    result['naqsh_squares'] = grouped_chars
    
    return result
EOL

# Write content to quran.py
cat > abjad_calculator/quran.py << 'EOL'
"""
Functions for Quranic verse calculation.
"""

from .core import calculate_abjad
from .display import calculate_arabic_text_with_table, calculate_multiple_texts_with_tables

def calculate_quranic_verse(verse_text, title=None, output_html=False, output_path=None):
    """
    Calculate abjad value for a Quranic verse and display as a table.
    
    Args:
        verse_text (str): The Quranic verse text
        title (str, optional): Title for the output
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        
    Returns:
        str: HTML string of the table
    """
    return calculate_arabic_text_with_table(
        verse_text, 
        title or "Quranic Verse Analysis",
        output_html,
        output_path
    )

def process_multiple_verses(verses_dict, output_html=False, output_path=None):
    """
    Process multiple Quranic verses and calculate their combined abjad value.
    
    Args:
        verses_dict (dict): Dictionary with verse identifiers as keys and verse text as values
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        
    Returns:
        str: Combined HTML string of all tables
    """
    return calculate_multiple_texts_with_tables(
        verses_dict,
        output_html,
        output_path or "quranic_verses.html"
    )
EOL

# Write content to __init__.py
cat > abjad_calculator/__init__.py << 'EOL'
"""
Arabic Abjad Calculator Package
A modular toolkit for Abjad numerical calculation in Arabic text.
"""

# Import main functions for easy access
from .core import calculate_abjad, calculate_special_properties
from .display import calculate_arabic_text_with_table, calculate_multiple_texts_with_tables
from .naqsh import generate_naqsh_dard_sar, generate_naqsh_dard_kamar
from .quran import calculate_quranic_verse, process_multiple_verses
from .utils import format_custom_output

# Version
__version__ = '1.0.0'
EOL

# Write content to main.py (Example file)
cat > main.py << 'EOL'
"""
Example usage of the Abjad Calculator library.
"""

import abjad_calculator as ac

def main():
    print("Abjad Calculator Examples")
    print("=" * 50)
    
    # Example 1: Calculate for a single Arabic phrase
    print("\n1. Calculate Abjad value for a single phrase")
    text = "بسم الله الرحمن الرحيم"
    result = ac.calculate_abjad(text)
    print(f"Total abjad value: {result['total_value']}")
    
    # Save as HTML table
    ac.calculate_arabic_text_with_table(text, "Bismillah", output_html=True)
    
    # Example 2: Generate a Naqsh for headache
    print("\n2. Generate Naqsh for headache")
    name = "م ح م د ف ی ر و ز ا ب ن ب ل ق ی س"
    naqsh_result = ac.generate_naqsh_dard_sar(name)
    print(f"Interleaved text: {naqsh_result['interleaved_text']}")
    print(f"Total abjad value: {naqsh_result['total_value']}")
    print("Naqsh squares:")
    for i, square in enumerate(naqsh_result['naqsh_squares']):
        print(f"  Square {i+1}: {square}")
    
    # Calculate special properties
    props = ac.calculate_special_properties(naqsh_result)
    print(f"Increment cell: {props['increment_cell']}")
    
    # Example 3: Process multiple Quranic verses
    print("\n3. Process multiple Quranic verses")
    verses = {
        "1:1": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "1:2": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"
    }
    ac.process_multiple_verses(verses, output_html=True)
    print("Multiple verse calculation complete. Check the HTML output.")

if __name__ == "__main__":
    main()
EOL

# Set execution permissions
chmod +x main.py

echo "Setup complete!"
echo "To run the example, type: python main.py"
echo "Make sure to install required dependencies: pip install pandas"