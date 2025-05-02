"""
display.py Display functions for Abjad calculation results.
"""
from typing import List
import pandas as pd

from .model import AbjadResult, LetterBreakdown, NaqshResult
from .core import calculate_abjad

def render_naqsh_html(naqsh_result: NaqshResult, output_html=False, output_path=None, show_summary=False, chars_per_row=18):
    """
    Render a naqsh calculation as HTML with tables and visual representation.
    
    Args:
        naqsh_result (dict): Result from naqsh generation
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        show_summary (bool): Whether to show detailed letter summary table
        chars_per_row (int): Maximum number of characters per row in letter tables
        
    Returns:
        str: HTML string with styled tables and naqsh visualization
    """
    letter_df, summary_df = create_abjad_dataframe(naqsh_result)
    
    # Create naqsh squares table
    squares_data = []
    for i, square in enumerate(naqsh_result.hurf_groups):
        squares_data.append({
            'Group #': i+1,
            'Content': square
        })
    
    squares_df = pd.DataFrame(squares_data)
    
    # Get special cell number
    increment_cell = naqsh_result.special_properties.increment_cell
    
    # Create letter-value tables with row splitting
    letter_tables_html = create_letter_value_tables(naqsh_result.breakdown, chars_per_row)
    
    # Generate HTML output
    html_output = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Naqsh {naqsh_result.naqsh_type}</title>
        <style>
            body {{
                font-family: 'Traditional Arabic', 'Amiri', Arial, sans-serif;
                margin: 20px;
                background-color: #f9f9f9;
                color: #333;
                direction: rtl;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 5px;
            }}
            h1, h2, h3 {{
                color: #295f9e;
                text-align: center;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                direction: rtl;
                border: 2px solid #8c9eff; /* Stronger table border */
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #bdbdbd; /* Visible cell borders */
                text-align: center;
            }}
            th {{
                background-color: #dbe1ff; /* Stronger header color */
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .highlight {{
                background-color: #fffde7;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 4px solid #fbc02d;
            }}
            .naqsh-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
                gap: 10px;
                margin: 20px 0;
            }}
            .naqsh-cell {{
                border: 1px solid #333;
                padding: 10px;
                text-align: center;
                font-size: 18px;
                background: #fff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            .special {{
                border: 2px solid #f44336;
            }}
            .letter-table {{
                margin-bottom: 20px;
                border: 2px solid #8c9eff; /* Stronger border for letter tables */
            }}
            .letter-table td {{
                min-width: 40px;
                font-size: 16px;
                border: 1px solid #bdbdbd; /* Visible borders for letter cells */
            }}
            .letter-row {{
                background-color: #e3f2fd; /* Lighter blue for letter row */
            }}
            .value-row {{
                background-color: #fff8e1; /* Light amber for value row */
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>نقش {naqsh_result.naqsh_type}</h1>
            
            <div class="section">
                <h2>بيانات النقش</h2>
                <table>
                    <tr>
                        <th>الاسم مع اسم الأم</th>
                        <td>{naqsh_result.name_with_mothers_name}</td>
                    </tr>
                    <tr>
                        <th>نوع النقش</th>
                        <td>{naqsh_result.naqsh_type}</td>
                    </tr>
                    <tr>
                        <th>بسطم</th>
                        <td>{naqsh_result.bastam_text}</td>
                    </tr>
                    <tr>
                        <th>حروف صوامت</th>
                        <td>{naqsh_result.huruf_sawamat}</td>
                    </tr>
                    <tr>
                        <th>النص المتداخل</th>
                        <td>{naqsh_result.interleaved_text}</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>حساب الجمل</h2>
                <div class="highlight">
                    <p><strong>القيمة الإجمالية:</strong> {naqsh_result.total_qamari_value}</p>
                    <p><strong>الإجمالي ناقص 12:</strong> {naqsh_result.special_properties.total_minus_12}</p>
                    <p><strong>القسمة على 3:</strong> الناتج {naqsh_result.special_properties.division_by_3.quotient}، الباقي {naqsh_result.special_properties.division_by_3.remainder}</p>
                    <p><strong>خانة الزيادة:</strong> {increment_cell}</p>
                </div>
                
                <h3>تفصيل الحساب</h3>
                {letter_tables_html}
                
                {summary_df.to_html(index=False) if show_summary else ''}
            </div>
            
            <div class="section">
                <h2>مربعات النقش</h2>
                <div class="naqsh-grid">
                    {' '.join(f'<div class="naqsh-cell{" special" if i+1 == increment_cell else ""}">{square}</div>' for i, square in enumerate(naqsh_result.hurf_groups))}
                </div>
                <p class="highlight"><strong>ملاحظة:</strong> المربع الملون باللون الأحمر هو خانة الزيادة.</p>
                
                <h3>جدول المربعات</h3>
                {squares_df.to_html(index=False)}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save to file if requested
    if output_html:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"HTML output saved to {output_path}")
    
    return html_output

def create_word_letter_value_tables(word_breakdown: List[AbjadResult], show_letters=False, chars_per_row=18):
    """
    Create HTML tables for letter/value representation with row splitting.
    
    Args:
        breakdown (list): List of letter/value dictionaries from calculation
        chars_per_row (int): Maximum characters per row
        
    Returns:
        str: HTML string with tables
    """
    tables_html = ""
    
    # Split the breakdown into chunks
    for i in range(0, len(word_breakdown), chars_per_row):
        chunk = word_breakdown[i:i+chars_per_row]
        
        # Start a table
        table_html = '<table class="qamari-malfuzi-table">\n'
        # letter row
        if show_letters:
            table_html += '<tr class="letter-row letter-value-row">\n'
            for word in chunk:
                len_word_breakdown = len(word.breakdown)
                for idx, letter in enumerate(word.breakdown):
                    class_letter_border = "light-letter-left-border"
                    if idx==len_word_breakdown-1:
                        class_letter_border = "dark-letter-left-border"
                    try:
                        table_html += f'<td class="{class_letter_border}">{letter.letter}</td>\n'
                    except Exception as ex:
                        print(word)
                        raise ex
            table_html += '</tr>\n'
            
            # Qamari Value row
            table_html += '<tr class="value-row letter-value-row qamari-value-row">\n'
            for word in chunk:
                len_word_breakdown = len(word.breakdown)
                for idx, letter in enumerate(word.breakdown):
                    class_letter_border = "light-letter-left-border"
                    if idx==len_word_breakdown-1:
                        class_letter_border = "dark-letter-left-border"
                    try:
                        table_html += f'<td class="{class_letter_border}">{letter.qamari_value}</td>\n'
                    except Exception as ex:
                        print(word)
                        raise ex
            table_html += '</tr>\n'

            # Malfuzi Value row
            table_html += '<tr class="value-row letter-value-row malfuzi-value-row">\n'
            for word in chunk:
                len_word_breakdown = len(word.breakdown)
                for idx, letter in enumerate(word.breakdown):
                    class_letter_border = "light-letter-left-border"
                    if idx==len_word_breakdown-1:
                        class_letter_border = "dark-letter-left-border"
                    try:
                        table_html += f'<td class="{class_letter_border}">{letter.malfuzi_value}</td>\n'
                    except Exception as ex:
                        print(word)
                        raise ex
            table_html += '</tr>\n'
        ###    
        table_html += '<tr class="word-row">\n'
        for word in chunk:
            table_html += f'<td colspan={len(word.breakdown)}>{word.original_text}</td>\n'
        table_html += '</tr>\n'

        # Qamari Value row
        table_html += '<tr class="value-row qamari-value-row">\n'
        for word in chunk:
            table_html += f'<td colspan={len(word.breakdown)}>{word.total_qamari_value}</td>\n'
        table_html += '</tr>\n'

        # Malfuzi Value row
        table_html += '<tr class="value-row malfuzi-value-row">\n'
        for word in chunk:
            table_html += f'<td colspan={len(word.breakdown)}>{word.total_malfuzi_value}</td>\n'
        table_html += '</tr>\n'

        
        # End the table
        table_html += '</table>\n'
        tables_html += table_html
    
    return tables_html

def create_abjad_dataframe(result: NaqshResult):
    """
    Convert abjad calculation result to pandas DataFrames.
    
    Args:
        result (dict): Result from calculate_abjad function
        
    Returns:
        tuple: (letter_df, summary_df) - Two DataFrames with detailed and summary information
    """
    # Create letter-by-letter DataFrame
    letter_data = []
    for item in result.breakdown:
        letter_data.append({
            'Letter': item.letter,
            'Qamari Value': item.qamari_value
        })
    
    letter_df = pd.DataFrame(letter_data)
    
    # Create summary DataFrame (for letter counts and totals)
    summary_data = []
    # for letter, data in sorted(result['verification'].items(), key=lambda x: ABJAD_VALUES[x[0]]):
    #     summary_data.append({
    #         'Letter': letter,
    #         'Count': data['count'],
    #         'Abjad Value': data['value'],
    #         'Subtotal': data['total']
    #     })
    
    summary_df = pd.DataFrame(summary_data)
    # summary_df = summary_df.sort_values(by='Abjad Value')
    
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
    letter_styled = letter_df.T.style.set_table_styles(styles).set_caption('Letter-by-Letter Breakdown')
    summary_styled = summary_df.style.set_table_styles(styles).set_caption('Summary by Letter')
    
    # Total values section
    totals_html = f"""
    <div style="margin:15px 0; padding:10px; background-color:#f2f2f2; border-radius:5px; font-family:Arial,sans-serif;">
        <p><strong>Total Abjad Value:</strong> {result['total_qamari_value']}</p>
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
    
    result = calculate_abjad(text)
    html_output = render_abjad_table_html(result, title)
    
    # Save to file if requested
    if output_html:
        path = output_path or f"abjad_calculation_{hash(text)}.html"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"HTML output saved to {path}")
    
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
    
    all_html = ""
    grand_qamari_total = 0
    
    for text_id, text in texts_dict.items():
        result: AbjadResult = calculate_abjad(text)
        grand_qamari_total += result.total_qamari_value
        html = render_abjad_table_html(result, f"Text {text_id}")
        all_html += html
    
    # Add grand total section
    grand_total_html = f"""
    <div style="margin:20px 0; padding:15px; background-color:#e8f4f8; border-radius:5px; font-family:Arial,sans-serif; text-align:center;">
        <h2>Grand Total for All Texts: {grand_qamari_total}</h2>
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
    
    return all_html

def create_quran_verse_html(result, title, chars_per_row=18):
    """
    Create HTML display for a Quranic verse with letter/value rows.
    
    Args:
        result (dict): Calculation result from calculate_abjad
        title (str): Title for the verse display
        chars_per_row (int): Maximum characters per row in letter tables
        
    Returns:
        str: HTML string
    """
    # Create letter-value tables
    return create_letter_value_tables(result['breakdown'], chars_per_row)