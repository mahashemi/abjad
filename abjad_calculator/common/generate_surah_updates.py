#!/usr/bin/env python3
"""Script to generate missing surah imports and entries for surah_factory.py"""

import os
from pathlib import Path

# Standard Quran chapter names with their numbers
quran_chapters = {
    12: ("Yusuf", "سورة يوسف", "12", "111"),
    13: ("Ar-Ra'd", "سورة الرعد", "13", "43"),
    14: ("Ibrahim", "سورة ابراهيم", "14", "52"),
    15: ("Al-Hijr", "سورة الحجر", "15", "99"),
    16: ("An-Nahl", "سورة النحل", "16", "128"),
    17: ("Al-Isra", "سورة الإسراء", "17", "111"),
    18: ("Al-Kahf", "سورة الكهف", "18", "110"),
    19: ("Maryam", "سورة مريم", "19", "98"),
    20: ("Ta-Ha", "سورة طه", "20", "135"),
    21: ("Al-Anbiya", "سورة الأنبياء", "21", "112"),
    22: ("Al-Hajj", "سورة الحج", "22", "78"),
    23: ("Al-Mu'minun", "سورة المؤمنون", "23", "118"),
    24: ("An-Nur", "سورة النور", "24", "64"),
    25: ("Al-Furqan", "سورة الفرقان", "25", "77"),
    26: ("Ash-Shu'ara", "سورة الشعراء", "26", "227"),
    27: ("An-Naml", "سورة النمل", "27", "93"),
    28: ("Al-Qasas", "سورة القصص", "28", "88"),
    29: ("Al-Ankabut", "سورة العنكبوت", "29", "69"),
    30: ("Ar-Rum", "سورة الروم", "30", "60"),
    31: ("Luqman", "سورة لقمان", "31", "34"),
    32: ("As-Sajdah", "سورة السجدة", "32", "30"),
    33: ("Al-Ahzab", "سورة الأحزاب", "33", "73"),
    34: ("Saba", "سورة سبأ", "34", "54"),
    35: ("Fatir", "سورة فاطر", "35", "45"),
    36: ("Ya-Sin", "سورة يس", "36", "83"),
    37: ("As-Saffat", "سورة الصافات", "37", "182"),
    38: ("Sad", "سورة ص", "38", "88"),
    39: ("Az-Zumar", "سورة الزمر", "39", "75"),
    40: ("Ghafir", "سورة غافر", "40", "85"),
    41: ("Fussilat", "سورة فصلت", "41", "54"),
    42: ("Ash-Shura", "سورة الشورى", "42", "53"),
    43: ("Az-Zukhruf", "سورة الزخرف", "43", "89"),
    44: ("Ad-Dukhan", "سورة الدخان", "44", "59"),
    45: ("Al-Jathiyah", "سورة الجاثية", "45", "37"),
    46: ("Al-Ahqaf", "سورة الأحقاف", "46", "35"),
    47: ("Muhammad", "سورة محمد", "47", "38"),
    48: ("Al-Fath", "سورة الفتح", "48", "29"),
    49: ("Al-Hujurat", "سورة الحجرات", "49", "18"),
    50: ("Qaf", "سورة ق", "50", "45"),
    51: ("Adh-Dhariyat", "سورة الذاريات", "51", "60"),
    52: ("At-Tur", "سورة الطور", "52", "49"),
    53: ("An-Najm", "سورة النجم", "53", "62"),
    54: ("Al-Qamar", "سورة القمر", "54", "55"),
    57: ("Al-Hadid", "سورة الحديد", "57", "29"),
    60: ("Al-Mumtahanah", "سورة الممتحنة", "60", "13"),
    61: ("As-Saff", "سورة الصف", "61", "14"),
    62: ("Al-Jumu'ah", "سورة الجمعة", "62", "11"),
    63: ("Al-Munafiqun", "سورة المنافقون", "63", "11"),
    64: ("At-Taghabun", "سورة التغابن", "64", "18"),
    65: ("At-Talaq", "سورة الطلاق", "65", "12"),
    66: ("At-Tahrim", "سورة التحريم", "66", "12"),
    67: ("Al-Mulk", "سورة الملك", "67", "30"),
    68: ("Al-Qalam", "سورة القلم", "68", "52"),
    69: ("Al-Haqqah", "سورة الحاقة", "69", "52"),
    70: ("Al-Ma'arij", "سورة المعارج", "70", "44"),
    71: ("Nuh", "سورة نوح", "71", "28"),
    72: ("Al-Jinn", "سورة الجن", "72", "28"),
    73: ("Al-Muzzammil", "سورة المزمل", "73", "20"),
    74: ("Al-Muddaththir", "سورة المدثر", "74", "56"),
    75: ("Al-Qiyamah", "سورة القيامة", "75", "40"),
    76: ("Al-Insan", "سورة الإنسان", "76", "31"),
    77: ("Al-Mursalat", "سورة المرسلات", "77", "50"),
}

# Map file names to standardized names
file_name_mapping = {
    "yusuf": 12,
    "raad": 13,  
    "ibrahim": 14,
    "hijr": 15,
    "nahl": 16,
    "isra": 17,
    "kahf": 18,
    "maryam": 19,
    "ta-ha": 20,
    "ambiya": 21,
    "hajj": 22,
    "momenoon": 23,
    "noor": 24,
    "furqaan": 25,
    "sho'ara": 26,
    "naml": 27,
    "qasas": 28,
    "ankaboot": 29,
    "room": 30,
    "luqman": 31,
    "sajdah": 32,
    "ahazab": 33,
    "saba": 34,
    "fatir": 35,
    "ya_seen": 36,
    "saffat": 37,
    "suad": 38,
    "zumar": 39,
    "ghafir": 40,
    "fusselat": 41,
    "shura": 42,
    "zukhruf": 43,
    "dukhan": 44,
    "jasiya": 45,
    "al-ahqaaf": 46,
    "mohammad": 47,
    "fat'h": 48,
    "al-hujraat": 49,
    "qaaf": 50,
    "zariyat": 51,
    "toor": 52,
    "najm": 53,
    "qamar": 54,
    "hadeed": 57,
    "mumtahina": 60,
    "as-saff": 61,
    "jumah": 62,
    "munafeqoon": 63,
    "taghabun": 64,
    "talaaq": 65,
    "tahreem": 66,
    "mulk": 67,
    "qalam": 68,
    "ha'qa": 69,
    "ma'arej": 70,
    "nooh": 71,
    "jinn": 72,
    "muzammil": 73,
    "mudassir": 74,
    "qayamat": 75,
    "dahr_[insaan]": 76,
}

def main():
    quran_lib = Path(__file__).parent.parent / "quran_library"
    
    # Get all chapter files
    chapter_files = sorted([f for f in quran_lib.glob("chapter_*.py") if f.name != "__init__.py"])
    
    # Extract chapter numbers from files
    existing_chapters = {}
    for f in chapter_files:
        parts = f.stem.split('_', 2)  # chapter_XXX_name
        if len(parts) >= 3:
            chapter_num = int(parts[1])
            name_part = '_'.join(parts[2:])
            existing_chapters[chapter_num] = name_part
    
    print("=" * 70)
    print("MISSING IMPORTS TO ADD TO surah_factory.py")
    print("=" * 70)
    print()
    print("Add these imports:")
    for ch_num in sorted(existing_chapters.keys()):
        print(f"    chapter_{ch_num:03d}_{existing_chapters[ch_num]},")
    
    print()
    print("=" * 70)
    print("MISSING TITLE DEFINITIONS")
    print("=" * 70)
    print()
    
    for ch_num in sorted(existing_chapters.keys()):
        if ch_num in quran_chapters:
            english, arabic, num, verses = quran_chapters[ch_num]
            var_name = existing_chapters[ch_num].replace('-', '_').replace("'", "").replace('[', '').replace(']', '')
            print(f'surah_{var_name}_title = "{arabic} - سورة {num} - عدد آياتها {verses}".strip()')
    
    print()
    print("=" * 70)
    print("MISSING DICTIONARY ENTRIES")
    print("=" * 70)
    print()
    
    for ch_num in sorted(existing_chapters.keys()):
        var_name = existing_chapters[ch_num].replace('-', '_').replace("'", "").replace('[', '').replace(']', '')
        print(f"    surah_{var_name}_title: chapter_{ch_num:03d}_{existing_chapters[ch_num]}.ayats,")

if __name__ == "__main__":
    main()
