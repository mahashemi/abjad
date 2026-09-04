/**
 * Abjad Constants - Shared across all modules
 */

const ABJAD_VALUES = {
    "ا": {"malfuzi": 111, "qamari": 1,   "bayenati": 110, "element": "atishi", "nature": "saad", "name": "الف"},
    "أ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110, "element": "atishi", "nature": "saad", "name": "الف"},
    "ٱ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110, "element": "atishi", "nature": "saad", "name": "الف"},
    "إ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110, "element": "atishi", "nature": "saad", "name": "الف"},
    "آ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110, "element": "atishi", "nature": "saad", "name": "الف"},
    "ب": {"malfuzi":   3, "qamari": 2,   "bayenati":   1, "element": "baadi",  "nature": "nahs", "name": "با"},
    "پ": {"malfuzi":   3, "qamari": 2,   "bayenati":   1, "element": "baadi",  "nature": "nahs", "name": "با"},
    "ج": {"malfuzi":  53, "qamari": 3,   "bayenati":  50, "element": "aabi",   "nature": "nahs", "name": "جیم"},
    "چ": {"malfuzi":  53, "qamari": 3,   "bayenati":  50, "element": "aabi",   "nature": "nahs", "name": "جیم"},
    "د": {"malfuzi":  35, "qamari": 4,   "bayenati":  31, "element": "khaki",  "nature": "saad", "name": "دال"},
    "ه": {"malfuzi":   6, "qamari": 5,   "bayenati":   1, "element": "atishi", "nature": "saad", "name": "ها"},
    "ة": {"malfuzi":   6, "qamari": 5,   "bayenati":   1, "element": "atishi", "nature": "saad", "name": "ها"},
    "ہ": {"malfuzi":   6, "qamari": 5,   "bayenati":   1, "element": "atishi", "nature": "saad", "name": "ها"},
    "ھ": {"malfuzi":   6, "qamari": 5,   "bayenati":   1, "element": "atishi", "nature": "saad", "name": "ها"},
    "و": {"malfuzi":  13, "qamari": 6,   "bayenati":   7, "element": "baadi",  "nature": "saad", "name": "واؤ"},
    "ؤ": {"malfuzi":  13, "qamari": 6,   "bayenati":   7, "element": "baadi",  "nature": "saad", "name": "واؤ"},
    "ز": {"malfuzi":   8, "qamari": 7,   "bayenati":   1, "element": "aabi",   "nature": "nahs", "name": "زا"},
    "ژ": {"malfuzi":   8, "qamari": 7,   "bayenati":   1, "element": "aabi",   "nature": "nahs", "name": "زا"},
    "ح": {"malfuzi":   9, "qamari": 8,   "bayenati":   1, "element": "khaki",  "nature": "saad", "name": "حا"},
    "ط": {"malfuzi":  10, "qamari": 9,   "bayenati":   1, "element": "atishi", "nature": "saad", "name": "طا"},
    "ي": {"malfuzi":  11, "qamari": 10,  "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "یا"},
    "ى": {"malfuzi":  11, "qamari": 10,  "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "یا"},
    "ی": {"malfuzi":  11, "qamari": 10,  "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "یا"},
    "ئ": {"malfuzi":  11, "qamari": 10,  "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "یا"},
    "ك": {"malfuzi": 101, "qamari": 20,  "bayenati":  81, "element": "aabi",   "nature": "saad", "name": "کاف"},
    "ک": {"malfuzi": 101, "qamari": 20,  "bayenati":  81, "element": "aabi",   "nature": "saad", "name": "کاف"},
    "گ": {"malfuzi": 101, "qamari": 20,  "bayenati":  81, "element": "aabi",   "nature": "saad", "name": "کاف"},
    "ل": {"malfuzi":  71, "qamari": 30,  "bayenati":  41, "element": "khaki",  "nature": "saad", "name": "لام"},
    "م": {"malfuzi":  90, "qamari": 40,  "bayenati":  50, "element": "atishi", "nature": "saad", "name": "میم"},
    "ن": {"malfuzi": 106, "qamari": 50,  "bayenati":  56, "element": "baadi",  "nature": "nahs", "name": "نون"},
    "س": {"malfuzi": 120, "qamari": 60,  "bayenati":  60, "element": "aabi",   "nature": "saad", "name": "سین"},
    "ع": {"malfuzi": 130, "qamari": 70,  "bayenati":  60, "element": "khaki",  "nature": "saad", "name": "عین"},
    "ف": {"malfuzi":  81, "qamari": 80,  "bayenati":   1, "element": "atishi", "nature": "nahs", "name": "فا"},
    "ص": {"malfuzi":  95, "qamari": 90,  "bayenati":   5, "element": "baadi",  "nature": "saad", "name": "صاد"},
    "ق": {"malfuzi": 181, "qamari": 100, "bayenati":  81, "element": "aabi",   "nature": "saad", "name": "قاف"},
    "ر": {"malfuzi": 201, "qamari": 200, "bayenati":   1, "element": "khaki",  "nature": "nahs", "name": "را"},
    "ڑ": {"malfuzi": 201, "qamari": 200, "bayenati":   1, "element": "khaki",  "nature": "nahs", "name": "را"},
    "ش": {"malfuzi": 360, "qamari": 300, "bayenati":  60, "element": "atishi", "nature": "nahs", "name": "شین"},
    "ت": {"malfuzi": 401, "qamari": 400, "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "تا"},
    "ٹ": {"malfuzi": 401, "qamari": 400, "bayenati":   1, "element": "baadi",  "nature": "saad", "name": "تا"},
    "ث": {"malfuzi": 501, "qamari": 500, "bayenati":   1, "element": "aabi",   "nature": "saad", "name": "ثا"},
    "خ": {"malfuzi": 601, "qamari": 600, "bayenati":   1, "element": "khaki",  "nature": "nahs", "name": "خا"},
    "ذ": {"malfuzi": 731, "qamari": 700, "bayenati":  31, "element": "atishi", "nature": "nahs", "name": "ذال"},
    "ض": {"malfuzi": 805, "qamari": 800, "bayenati":   5, "element": "baadi",  "nature": "nahs", "name": "ضاد"},
    "ظ": {"malfuzi": 901, "qamari": 900, "bayenati":   1, "element": "aabi",   "nature": "nahs", "name": "ظا"},
    "غ": {"malfuzi":1060, "qamari":1000, "bayenati":  60, "element": "khaki",  "nature": "nahs", "name": "غین"}
};

const ELEMENT_INFO = {
    "atishi": { name: "آتشی", meaning: "Fire", icon: "🔥", color: "#8B0000" },
    "baadi": { name: "هوایی", meaning: "Air", icon: "💨", color: "#4B0082" },
    "aabi": { name: "آبی", meaning: "Water", icon: "💧", color: "#00008B" },
    "khaki": { name: "خاکی", meaning: "Earth", icon: "🌍", color: "#006400" }
};

const NATURE_INFO = {
    "saad": { name: "سعد", meaning: "Auspicious", color: "#228B22" },
    "nahs": { name: "نحس", meaning: "Inauspicious", color: "#8B0000" }
};

const YA_HAMZA = 'ئ';
const HAMZA = 'ء';
