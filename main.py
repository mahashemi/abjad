"""
Example usage of the Abjad Calculator library.
"""
import os
import abjad_calculator as ac
from abjad_calculator.quran_library import (
    sura_al_fatiha,
    sura_al_masad,
    sura_al_falaq,
    sura_al_nasr,
    surah_al_ikhlas,
    surah_al_naba,
    surah_al_nas)

def huruf_sawamat_html_example(name, bastam_type):
    """Example showing HTML output for Huruf Sawamat naqsh"""

    
    # Generate naqsh for person's name
    
    ac.create_output_dir('output')
    # Generate HTML report for dard sar (headache)
    html = ac.generate_sawamat_naqsh_html(
        name_with_mothers_name=name,
        dard_location=bastam_type,
        output_html=True,
        show_summary=False,  # Hide detailed summary table
        chars_per_row=9,    # Set characters per row
        output_path=f"output/naqsh_sawamat_{bastam_type}.html"
    )
    print("Huruf Sawamat Naqsh HTML report generated successfully!")
    
    # You can also generate for back pain
    # ac.generate_sawamat_naqsh_html(name, bastam_type="kamar", output_html=True)

def main():
    bismillah = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ".strip()
    print("Abjad Calculator")
    print("=" * 50)
    
    # Example 1: Calculate for a single Arabic phrase
    # print("\n1. Calculate Abjad value for a single phrase")
    # text = "بسم الله الرحمن الرحيم"
    # result = ac.calculate_abjad(text)
    # print(f"Total abjad value: {result['total_value']}")
    
    # # Save as HTML table
    # ac.calculate_arabic_text_with_table(text, "Bismillah", output_html=True)
    
    # Example 2: Generate a Naqsh for headache
    print("\n2. Generate Naqsh for headache")
    # name = " م ح م د ف ی ر و ز ا ب ن ب ل ق ی س ج ہ ا ن"
    name = " ج ا ر ی ہ ر ض ا ع د ی ل ہ ش و ک ت "
    dard_location = "kamar"
    # huruf_sawamat_html_example(name=name, bastam_type=dard_location.upper())


    # naqsh_result = ac.generate_naqsh_dard_sar(name)
    # print(f"Interleaved text: {naqsh_result['interleaved_text']}")
    # print(f"Total abjad value: {naqsh_result['total_value']}")
    # print("Naqsh squares:")
    # for i, square in enumerate(naqsh_result['naqsh_squares']):
    #     print(f"  Square {i+1}: {square}")
    
    # Calculate special properties
    # props = ac.calculate_special_properties(naqsh_result)
    # print(f"Increment cell: {props['increment_cell']}")
    
    # Example 3: Process multiple Quranic verses
    print("\n3. Process multiple Quranic verses")
    surah_fatiha_title = "سورة الفاتحة - سورة 1 - عدد آياتها 7 ".strip()
    surah_qalam_title = "سورة القلم - سورة 68 - عدد آياتها 52 ".strip()
    surah_al_naba_title = "سورة النبأ - سورة 78 - عدد آياتها 40".strip()
    surat_kafiroon_title = "سورة الكافرون - سورة 109 - عدد آياتها 6".strip()
    surah_al_nasr_title = "سورة النصر - سورة 110 - عدد آياتها 3".strip()
    surah_al_masad_title = "سورة المسد - سورة 111 - عدد آياتها 5 ".strip()
    surah_al_ikhlas_title = "سورة الإخلاص - سورة 112 - عدد آياتها 4".strip()
    surah_al_falaq_title = "سورة الفلق - سورة 113 - عدد آياتها 5".strip()
    surah_al_nas_title = "سورة الناس - سورة 114 - عدد آياتها 6".strip()

    quran = {
        surah_fatiha_title: sura_al_fatiha.ayats,
        surah_al_falaq_title: sura_al_falaq.ayats,
        surah_al_masad_title: sura_al_masad.ayats,
        surah_al_ikhlas_title: surah_al_ikhlas.ayats,
        surah_al_naba_title: surah_al_naba.ayats,
        surah_al_nas_title: surah_al_nas.ayats,
        surah_al_nasr_title: sura_al_nasr.ayats,
    }
    
    
    os.makedirs("output/quran/", exist_ok=True)

    for title, ayats in quran.items():
        # print(verses_surah_kafirun)
        ac.process_multiple_verses(
            bismillah,
            title,
            ayats,
            output_html=True,
            chars_per_row=14,      # 18 characters per row
            show_summary=False,    # Show detailed summary for this longer analysis
            output_path=f"output/quran/{title}.html")
    print("Multiple Verse:calculation complete. Check the HTML output.")

if __name__ == "__main__":
    main()
