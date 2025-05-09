"""
quran.py Functions for Quranic verse calculation.
"""

import json
import os
from typing import List
from dataclasses import asdict
from .template.quran_template import quran_html_template_start
from ...common.model import AbjadResult, LetterBreakdown
from ...common.core import calculate_abjad
from ...common.display import (
    create_word_letter_value_tables,
    create_quran_verse_html,
    calculate_arabic_text_with_table,
    calculate_multiple_texts_with_tables,
)


def calculate_quranic_verse(
    verse_text,
    title=None,
    output_html=False,
    output_path=None,
    show_summary=False,
    chars_per_row=18,
):
    """
    Calculate abjad value for a Quranic verse and display as a table with improved formatting.

    Args:
        verse_text (str): The Quranic verse text
        title (str, optional): Title for the output
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        show_summary (bool): Whether to show detailed letter summary table
        chars_per_row (int): Maximum number of characters per row in letter tables

    Returns:
        str: HTML string of the table
    """

    # Calculate abjad value
    result = calculate_abjad(verse_text)

    # Generate HTML output
    html_output = create_quran_verse_html(
        result, title, output_html, output_path, show_summary, chars_per_row
    )

    return html_output


def process_multiple_verses(
    bismillah,
    surat_name,
    verses_list,
    output_html=False,
    output_path=None,
    debug=False,
    chars_per_row=18,
):
    """
    Process multiple Quranic verses and calculate their combined abjad value.

    Args:
        verses_dict (dict): Dictionary with verse identifiers as keys and verse text as values
        output_html (bool): Whether to save HTML output to a file
        output_path (str, optional): Path to save HTML output
        show_summary (bool): Whether to show detailed letter summary table
        chars_per_row (int): Maximum number of characters per row in letter tables

    Returns:
        str: Combined HTML string of all tables
    """
    quran_html = quran_html_template_start
    quran_data_html = ""
    grand_qamari_total = 0
    grand_malfuzi_total = 0
    grand_bayenati_total = 0
    for verse_object in verses_list:
        verse_number = verse_object.get("verse_number")
        arabic = verse_object.get("arabic_text")
        urdu = verse_object.get("urdu_text")
        farsi = verse_object.get("persian_text")
        english = verse_object.get("english_text")
        transliteration = verse_object.get("transliteration")

        result_verse: AbjadResult = calculate_abjad(arabic)

        if debug:
            debug_output_folder = f"debug/{surat_name}/{verse_number}"
            os.makedirs(debug_output_folder, exist_ok=True)
            debug_output_path = os.path.join(debug_output_folder, "result.json")
            with open(debug_output_path, "w") as f:
                json.dump(asdict(result_verse), f, ensure_ascii=False, indent=4)
            print(f"debug output saved to {debug_output_path}")

        # print(result)
        grand_qamari_total += result_verse.total_qamari_value
        grand_malfuzi_total += result_verse.total_malfuzi_value
        grand_bayenati_total += result_verse.total_bayenati_value

        word_abjad_breakdown: List[AbjadResult] = []
        for idx, word in enumerate(arabic.split(" ")):
            if not word:
                continue
            result_word: AbjadResult = calculate_abjad(word)
            word_abjad_breakdown.append(result_word)
            # orig_word_text: str = result_word.original_text
            # word_total_qamari_value: int = result_word.total_qamari_value
            # word_total_malfuzi_value: int = result_word.total_malfuzi_value
            # word_total_bayenati_value: int = result_word.total_bayenati_value

            # word_abjad_breakdown.append(
            #     LetterBreakdown(
            #         letter=orig_word_text,
            #         qamari_value=word_total_qamari_value,
            #         malfuzi_value=word_total_malfuzi_value,
            #         bayenati_value=word_total_bayenati_value
            #     )
            # )

            # print(result_word)
            # if idx == 3:
            #     break
            # print('-'*20)

        word_abjad_tables_html = create_word_letter_value_tables(
            word_breakdown=word_abjad_breakdown,
            show_letters=debug,
            chars_per_row=chars_per_row,
        )

        # title = f"آية "

        # Main content for the verse
        content_html = f"""
<div class="verse-container">
    <div class="original-text">
        <p class="arabic-text">{result_verse.original_text} <span class='ayah-marker'>{verse_number}</span></p>
    </div>
</div>
"""

        verse_calculation_html = f"""
<div class="calculation">
    {word_abjad_tables_html}
</div>
"""

        translations_html = """
<div class="translations">
"""
        if urdu:
            translations_html += f"""
<p class='right-to-left'><span class="translation-title">اردو</span>{urdu}</p>
"""

        if farsi:
            translations_html += f"""
<p class='right-to-left'><span class="translation-title">فارسی</span>{farsi}</p>
"""

        if english:
            translations_html += f"""
<p class='left-to-right'><span class="translation-title">English</span>{english}</p>
"""

        if transliteration:
            translations_html += f"""
<p class='left-to-right'><span class="translation-title left-to-right">Transliteration</span>{transliteration}</p>
"""

        if result_verse.total_qamari_value:
            translations_html += f"""<div class='adad-row'>
    <div class='total-qamari-span'><span class="translation-title">قمري عدد</span> <strong class='total-value'>{result_verse.total_qamari_value}</strong></div>
    <div class='total-bayenati-span'><span class="translation-title">باطني عدد</span> <strong class='total-value'>{result_verse.total_bayenati_value}</strong></div>
    <div class='total-malfuzi-span'><span class="translation-title">ملفوظي عدد</span> <strong class='total-value'>{result_verse.total_malfuzi_value}</strong></div>
</div>
"""

        translations_html += """
</div>
"""

        # Add to the combined HTML
        quran_data_html += f"""
<div class="verse-section">
    {content_html}
    {verse_calculation_html}
    {translations_html}
</div>
"""

        # Add to the combined HTML
        # quran_html += f"""
        # <div class="verse-section">
        #     {verse_html}
        # </div>
        # """
        # break

    # Add grand total section
    quran_data_html += f"""
<div class="grand-total">
    <div class='qamari-grand-total'>
        <h3>مجموع القمري</h3>
        <p><strong>{grand_qamari_total}</strong></p>
    </div>
    <div class='batini-grand-total'>
        <h3>مجموع الباطني</h3>
        <p><strong>{grand_bayenati_total}</strong></p>
    </div>
    <div class='malfuzi-grand-total'>
        <h3>مجموع الملفوظي</h3>
        <p><strong>{grand_malfuzi_total}</strong></p>
    </div>
</div>
"""

    quran_html = quran_html.replace("{{bismillah}}", bismillah)
    quran_html = quran_html.replace("{{surat_name}}", surat_name)
    quran_html = quran_html.replace("{{quran_data_html}}", quran_data_html)

    # Save to file if requested
    if output_html:
        path = output_path or "quranic_verses.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(quran_html)
        print(f"HTML output saved to {path}")

    return quran_html
