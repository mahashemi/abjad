/**
 * Abjad Calculator - JavaScript Port
 * Ported from Python abjad_calculator/common/core.py
 */

const ABJAD_VALUES = {
    "ا": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "أ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "ٱ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "إ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "آ": {"malfuzi": 111, "qamari": 1,   "bayenati": 110},
    "ب": {"malfuzi":   3, "qamari": 2,   "bayenati":   1},
    "ج": {"malfuzi":  53, "qamari": 3,   "bayenati":  50},
    "د": {"malfuzi":  35, "qamari": 4,   "bayenati":  31},
    "ه": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},
    "ة": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},
    "ہ": {"malfuzi":   6, "qamari": 5,   "bayenati":   1},
    "و": {"malfuzi":  13, "qamari": 6,   "bayenati":   7},
    "ؤ": {"malfuzi":  13, "qamari": 6,   "bayenati":   7},
    "ز": {"malfuzi":   8, "qamari": 7,   "bayenati":   1},
    "ح": {"malfuzi":   9, "qamari": 8,   "bayenati":   1},
    "ط": {"malfuzi":  10, "qamari": 9,   "bayenati":   1},
    "ي": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},
    "ى": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},
    "ی": {"malfuzi":  11, "qamari": 10,  "bayenati":   1},
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
    "غ": {"malfuzi":1060, "qamari":1000, "bayenati":  60}
};

const YA_HAMZA = 'ئ';
const HAMZA = 'ء';

const REMOVE_CHARS = [
    'ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ',
    'ٓ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۝', '۞',
    '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ',
    '۩', '۪', '۫', '۬', 'ۭ', 'ٗ', 'ء', '<br/>',
    ' ', '\n', '\t', '\r', 'ـ'
];

function stripDiacritics(s) {
    return s.replace(/[\u064B-\u065F\u0670]/g, '');
}

function cleanText(text) {
    for (const char of REMOVE_CHARS) {
        text = text.split(char).join('');
    }
    return stripDiacritics(text);
}

function calculateAbjad(text) {
    const originalText = text;
    const cleanedText = cleanText(text);

    const result = {
        original_text: originalText,
        cleaned_text: cleanedText,
        total_qamari_value: 0,
        total_malfuzi_value: 0,
        total_bayenati_value: 0,
        breakdown: [],
        letter_counts: {},
        verification: {},
        verification_total: 0
    };

    for (const char of cleanedText) {
        if (!char.trim()) continue;

        let processedChar = char;
        if (processedChar === YA_HAMZA) {
            processedChar = HAMZA;
        }

        let qamariValue = 0;
        let malfuziValue = 0;
        let bayenatiValue = 0;

        if (ABJAD_VALUES[processedChar]) {
            qamariValue = ABJAD_VALUES[processedChar].qamari;
            malfuziValue = ABJAD_VALUES[processedChar].malfuzi;
            bayenatiValue = ABJAD_VALUES[processedChar].bayenati;
        }

        result.breakdown.push({
            letter: processedChar,
            qamari_value: qamariValue,
            malfuzi_value: malfuziValue,
            bayenati_value: bayenatiValue
        });

        result.total_qamari_value += qamariValue;
        result.total_malfuzi_value += malfuziValue;
        result.total_bayenati_value += bayenatiValue;

        result.letter_counts[processedChar] = (result.letter_counts[processedChar] || 0) + 1;
    }

    let verificationTotal = 0;
    for (const [letter, count] of Object.entries(result.letter_counts)) {
        const value = ABJAD_VALUES[letter] ? ABJAD_VALUES[letter].qamari : 0;
        const subTotal = count * value;
        verificationTotal += subTotal;
        result.verification[letter] = {
            count: count,
            qamari_value: value,
            total: subTotal
        };
    }
    result.verification_total = verificationTotal;

    return result;
}

function calculateMusallasProperties(abjadResult) {
    const total = abjadResult.total_qamari_value;
    const totalMinus12 = total - 12;
    const quotient = Math.floor(totalMinus12 / 3);
    const remainder = totalMinus12 % 3;
    const incrementCell = remainder === 2 ? 2 : 7;

    return {
        total_minus_12: totalMinus12,
        division_by_3: { quotient: quotient, remainder: remainder },
        increment_cell: incrementCell
    };
}

function calculateWords(text) {
    const words = text.split(/\s+/).filter(w => w.trim());
    const results = [];

    for (const word of words) {
        const wordResult = calculateAbjad(word);
        results.push({
            original_text: word,
            cleaned_text: wordResult.cleaned_text,
            total_qamari_value: wordResult.total_qamari_value,
            total_malfuzi_value: wordResult.total_malfuzi_value,
            total_bayenati_value: wordResult.total_bayenati_value,
            breakdown: wordResult.breakdown
        });
    }

    return results;
}

function generateWordCardsHtml(words) {
    if (!words.length) return '';

    let html = '<div class="word-cards-row">';

    for (const word of words) {
        let letterDetailHtml = '';
        if (word.breakdown && word.breakdown.length > 0) {
            let letterItems = '';
            for (let idx = 0; idx < word.breakdown.length; idx++) {
                const letter = word.breakdown[idx];
                const borderClass = idx < word.breakdown.length - 1 ? 'letter-item-light' : 'letter-item-dark';
                letterItems += '<div class="letter-item ' + borderClass + '"><span class="letter-char">' + letter.letter + '</span><span class="letter-qamari">' + letter.qamari_value + '</span><span class="letter-malfuzi">' + letter.malfuzi_value + '</span></div>';
            }
            letterDetailHtml = '<div class="letter-breakdown">' + letterItems + '</div>';
        }

        html += '<div class="word-card" onclick="toggleLetterDetail(this)">' + letterDetailHtml + '<div class="word-text arabic-font">' + word.original_text + '</div><div class="word-values"><span class="value-qamari">' + word.total_qamari_value + '</span><span class="value-malfuzi">' + word.total_malfuzi_value + '</span></div></div>';
    }

    html += '</div>';
    return html;
}

function generateGrandTotalHtml(result) {
    return '<div class="translations"><div class="adad-row grand-total"><div class="total-qamari-span"><span class="translation-title">مجموع القمري</span> <strong class="total-value">' + result.total_qamari_value + '</strong></div><div class="total-bayenati-span"><span class="translation-title">مجموع الباطني</span> <strong class="total-value">' + result.total_bayenati_value + '</strong></div><div class="total-malfuzi-span"><span class="translation-title">مجموع الملفوظي</span> <strong class="total-value">' + result.total_malfuzi_value + '</strong></div></div></div>';
}

function renderCalculatorResult(container, text) {
    if (!text.trim()) {
        container.innerHTML = '<div class="error">الرجاء إدخال نص عربي</div>';
        return;
    }

    const words = calculateWords(text);
    const fullResult = calculateAbjad(text);

    let html = '<div class="calculator-result">';
    html += '<div class="arabic-text arabic-font" style="margin-bottom:15px;">' + text + '</div>';
    html += generateWordCardsHtml(words);
    html += generateGrandTotalHtml(fullResult);
    html += '</div>';

    container.innerHTML = container.innerHTML + html;
}
