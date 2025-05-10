"""
Constants and mappings for the Abjad Calculator.
"""

ABJAD_VALUES = {
    "ا": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "أ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "ٱ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "إ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "آ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},  # Alif variations

    "ب": {"malfuzi":   3, "qamari": 2,   "bayenati":   1},
    "ج": {"malfuzi":  53, "qamari": 3,   "bayenati":  50},
    "د": {"malfuzi":  35, "qamari": 4,   "bayenati":  31},

    "ه": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},
    "ة": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},
    "ہ": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},  # Ha variations

    "و": {"malfuzi":  13, "qamari": 6,   "bayenati":   7},
    "ؤ": {"malfuzi":  13, "qamari": 6,   "bayenati":   7},

    "ز": {"malfuzi":   8, "qamari": 7,   "bayenati":   1},
    "ح": {"malfuzi":   9, "qamari": 8,   "bayenati":   1},
    "ط": {"malfuzi":  10, "qamari": 9,   "bayenati":   1},

    "ي": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},
    "ى": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},
    "ی": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},  # Ya variations

    "ك": {"malfuzi": 101, "qamari": 20,  "bayenati":  81},
    "ل": {"malfuzi":  71, "qamari": 30,  "bayenati":  41},
    "م": {"malfuzi":  90, "qamari": 40,  "bayenati":  50},
    "ن": {"malfuzi": 106, "qamari": 50,  "bayenati":  56},
    "س": {"malfuzi": 120, "qamari": 60,  "bayenati":  60},
    "ع": {"malfuzi": 130, "qamari": 70,  "bayenati":  60},
    "ف": {"malfuzi":  81, "qamari": 80,  "bayenati":   1},
    "ص": {"malfuzi":  95, "qamari": 90,  "bayenati":   5},
    "ق": {"malfuzi": 181, "qamari": 100, "bayenati":  81},
    "ر": {"malfuzi": 201, "qamari": 200, "bayenati":   1},
    "ش": {"malfuzi": 360, "qamari": 300, "bayenati":  60},
    "ت": {"malfuzi": 401, "qamari": 400, "bayenati":   1},
    "ث": {"malfuzi": 501, "qamari": 500, "bayenati":   1},
    "خ": {"malfuzi": 601, "qamari": 600, "bayenati":   1},
    "ذ": {"malfuzi": 731, "qamari": 700, "bayenati":  31},
    "ض": {"malfuzi": 805, "qamari": 800, "bayenati":   5},
    "ظ": {"malfuzi": 901, "qamari": 900, "bayenati":   1},
    "غ": {"malfuzi":1060, "qamari":1000, "bayenati":  60},
}
YA_HAMZA = 'ئ'
HAMZA = 'ء'

REMOVE_CHARS = [
    # Tashkeel (diacritics)
    'ً', 'ٌ', 'ٍ',  # tanween: Fathatan, Dammatan, Kasratan
    'َ', 'ُ', 'ِ',  # short vowels: Fatha, Damma, Kasra
    'ّ', 'ْ',        # Shadda, Sukun
    'ٰ',             # superscript alif

    # Additional Quranic diacritics (used in Uthmani script)
    'ٓ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۝', '۞',
    '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ',
    '۩', '۪', '۫', '۬', 'ۭ'," 	ٗ"

    # Hamza (standalone)
    'ء',

    # Whitespace and control characters
    ' ', '\n', '\t', '\r', '\u200c', '\u200d', '\u202c'
]


# Pre-defined texts for naqsh generation
PRESET_TEXTS = {
    "bastam_dard_sar": "ب س ت م د ر د س ر",
    "bastam_dard_kamar": "ب س ت م د ر د ك م ر",
    "huruf_sawamat": "ا ح د ر س ص ط ع ك ل م و ه",
}
