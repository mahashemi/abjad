/**
 * Basics Page - Educational Tables
 * Reuses Quran surah page design patterns
 * Constants loaded from abjad-constants.js
 */

function cleanText(text) {
    const REMOVE_CHARS = ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ', 'ٓ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۝', '۞', '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ', '۩', '۪', '۫', '۬', 'ۭ', 'ٗ', 'ء', '<br/>', ' ', '\n', '\t', '\r', 'ـ'];
    for (const char of REMOVE_CHARS) {
        text = text.split(char).join('');
    }
    return text.replace(/[\u064B-\u065F\u0670]/g, '');
}

function calculateAbjad(text) {
    const cleanedText = cleanText(text);
    const result = {
        breakdown: [],
        total_qamari_value: 0,
        total_malfuzi_value: 0
    };
    for (const char of cleanedText) {
        if (!char.trim()) continue;
        let processedChar = char;
        if (processedChar === YA_HAMZA) processedChar = HAMZA;
        let qamariValue = 0;
        let malfuziValue = 0;
        if (ABJAD_VALUES[processedChar]) {
            qamariValue = ABJAD_VALUES[processedChar].qamari;
            malfuziValue = ABJAD_VALUES[processedChar].malfuzi;
        }
        result.breakdown.push({ letter: processedChar, qamari_value: qamariValue, malfuzi_value: malfuziValue });
        result.total_qamari_value += qamariValue;
        result.total_malfuzi_value += malfuziValue;
    }
    return result;
}

function toggleLetterDetail(card) {
    const breakdown = card.querySelector('.letter-breakdown');
    if (breakdown) {
        breakdown.classList.toggle('show');
    }
}

function renderBasicsPage(container) {
    let html = '<div class="container basics-container">';

    // Page header
    html += '<div class="surah_header surah_name container arabic-font">';
    html += '<div class="surat-name-value name-elements">مقدمة في نظام الجمل العددي</div>';
    html += '</div>';

    // Quran Ayat section
    html += '<div class="verse-section quran-ayat-section">';
    html += '<div class="toggle-section-title">آيات من القرآن الكريم</div>';
    html += '<div class="ayat-container">';
    html += '<div class="quran-ayat">';
    html += '<div class="ayat-text arabic-font">وَكُلَّ شَيْءٍ عَدَدْنَاهُ كِتَابًا</div>';
    html += '<div class="ayat-reference">النبأ - آية 29</div>';
    html += '<div class="ayat-translation">"And We have counted everything in a register."</div>';
    html += '</div>';

    html += '<div class="quran-ayat">';
    html += '<div class="ayat-text arabic-font">كِتَابٌ مَّرْقُومٌ</div>';
    html += '<div class="ayat-reference">المطففين - آية 20</div>';
    html += '<div class="ayat-translation">"A written record."</div>';
    html += '</div>';

    html += '</div>';
    html += '</div>';

    // Example / Explanation section
    html += '<div class="verse-section example-section">';
    html += '<div class="toggle-section-title">مثال (Example)</div>';
    html += '<div class="example-tile">';
    html += '<div class="example-word arabic-font">بِسْمِ</div>';
    html += '<div class="example-breakdown">';
    html += '<div class="example-letter-group">';
    html += '<span class="example-letter arabic-font">ب</span>';
    html += '<span class="example-arrow">↓</span>';
    html += '<span class="example-values">';
    html += '<span class="example-value-col"><span class="value-qamari" title="قمري (Qamari)">2</span><span class="example-label qamari-label">قمري</span></span>';
    html += '<span class="example-value-col"><span class="value-malfuzi" title="ملفوظي (Malfuzi)">3</span><span class="example-label malfuzi-label">ملفوظي</span></span>';
    html += '</span>';
    html += '</div>';
    html += '<div class="example-letter-group">';
    html += '<span class="example-letter arabic-font">س</span>';
    html += '<span class="example-arrow">↓</span>';
    html += '<span class="example-values">';
    html += '<span class="example-value-col"><span class="value-qamari" title="قمري (Qamari)">60</span><span class="example-label qamari-label">قمري</span></span>';
    html += '<span class="example-value-col"><span class="value-malfuzi" title="ملفوظي (Malfuzi)">120</span><span class="example-label malfuzi-label">ملفوظي</span></span>';
    html += '</span>';
    html += '</div>';
    html += '<div class="example-letter-group">';
    html += '<span class="example-letter arabic-font">م</span>';
    html += '<span class="example-arrow">↓</span>';
    html += '<span class="example-values">';
    html += '<span class="example-value-col"><span class="value-qamari" title="قمري (Qamari)">40</span><span class="example-label qamari-label">قمري</span></span>';
    html += '<span class="example-value-col"><span class="value-malfuzi" title="ملفوظي (Malfuzi)">90</span><span class="example-label malfuzi-label">ملفوظي</span></span>';
    html += '</span>';
    html += '</div>';
    html += '</div>';
    html += '<div class="example-total arabic-font">المجموع: <span class="value-qamari">102</span> | <span class="value-malfuzi">213</span></div>';
    html += '<p class="example-note">كل حرف عربي له قيمة عددية بنظامين: <strong class="qamari-text">القمري</strong> (Qamari) و <strong class="malfuzi-text">الملفوظي</strong> (Malfuzi). انقر على البطاقات لرؤية التفاصيل.</p>';
    html += '<p class="example-note-en">Each Arabic letter has a numerical value in two systems: <strong class="qamari-text">Qamari</strong> and <strong class="malfuzi-text">Malfuzi</strong>. Click the cards to see the breakdown.</p>';
    html += '</div>';
    html += '</div>';

    // Section 1: Qamari Table (static cards - no click)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">جدول القمري (Qamari Values)</div>';
    html += '<div class="word-cards-row">';

    const qamariGroups = {};
    const allLetters = ["ا", "ب", "پ", "ج", "چ", "د", "ه", "ة", "ھ", "و", "ؤ", "ز", "ژ", "ح", "ط", "ي", "ی", "ئ", "ك", "ک", "گ", "ل", "م", "ن", "س", "ع", "ف", "ص", "ق", "ر", "ڑ", "ش", "ت", "ٹ", "ث", "خ", "ذ", "ض", "ظ", "غ"];

    for (const letter of allLetters) {
        const data = ABJAD_VALUES[letter];
        if (data) {
            const key = data.qamari;
            if (!qamariGroups[key]) {
                qamariGroups[key] = { letters: [], name: data.name };
            }
            qamariGroups[key].letters.push(letter);
        }
    }

    const sortedKeys = Object.keys(qamariGroups).sort((a, b) => parseInt(a) - parseInt(b));
    for (const qamari of sortedKeys) {
        const group = qamariGroups[qamari];
        html += '<div class="word-card" style="cursor:default;">';
        html += '<div class="word-text arabic-font">' + group.letters.join('، ') + '</div>';
        html += '<div class="word-values"><span class="value-qamari" title="قمري (Qamari)">' + qamari + '</span></div>';
        html += '</div>';
    }

    html += '</div></div>';

    // Section 2: Malfuzi Table (click to expand - like Quran word cards)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">جدول الملفوظي (Malfuzi Values)</div>';
    html += '<div class="word-cards-row">';

    const malfuziGroups = {};
    for (const letter of allLetters) {
        const data = ABJAD_VALUES[letter];
        if (data) {
            const key = data.malfuzi;
            if (!malfuziGroups[key]) {
                malfuziGroups[key] = { letters: [], name: data.name, qamari: data.qamari, nameBreakdown: calculateAbjad(data.name) };
            }
            malfuziGroups[key].letters.push(letter);
        }
    }

    // Sort by actual qamari value (same order as Qamari table)
    const sortedMalfuziGroups = Object.entries(malfuziGroups).sort((a, b) => a[1].qamari - b[1].qamari);
    for (const [malfuzi, group] of sortedMalfuziGroups) {
        const nameLetters = group.nameBreakdown.breakdown;

        let letterDetailHtml = '';
        if (nameLetters.length > 0) {
            let letterItems = '';
            for (let idx = 0; idx < nameLetters.length; idx++) {
                const letter = nameLetters[idx];
                const borderClass = idx < nameLetters.length - 1 ? 'letter-item-light' : 'letter-item-dark';
                letterItems += '<div class="letter-item ' + borderClass + '"><span class="letter-char">' + letter.letter + '</span><span class="letter-qamari">' + letter.qamari_value + '</span><span class="letter-malfuzi">' + letter.malfuzi_value + '</span></div>';
            }
            letterDetailHtml = '<div class="letter-breakdown">' + letterItems + '</div>';
        }

        html += '<div class="word-card" onclick="toggleLetterDetail(this)">';
        html += letterDetailHtml;
        html += '<div class="word-text arabic-font">' + group.name + '</div>';
        html += '<div class="word-values"><span class="value-qamari" title="قمري (Qamari)">' + group.qamari + '</span><span class="value-malfuzi" title="ملفوظي (Malfuzi)">' + malfuzi + '</span></div>';
        html += '</div>';
    }

    html += '</div></div>';

    // Section 3: Elements x Nature Table (element on right - first column in RTL)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">العناصر والطبائع (Elements & Nature)</div>';
    html += '<div class="table-wrapper"><table class="basics-table element-table">';
    html += '<thead><tr><th>عُنْصُر</th><th>سعد</th><th>نحس</th></tr></thead>';
    html += '<tbody>';

    const elemNatMatrix = {};
    for (const elemKey of Object.keys(ELEMENT_INFO)) {
        elemNatMatrix[elemKey] = { saad: [], nahs: [] };
    }

    for (const letter of allLetters) {
        const data = ABJAD_VALUES[letter];
        if (data && data.element && data.nature) {
            if (elemNatMatrix[data.element]) {
                elemNatMatrix[data.element][data.nature].push(letter);
            }
        }
    }

    for (const [elemKey, info] of Object.entries(ELEMENT_INFO)) {
        const matrix = elemNatMatrix[elemKey];
        html += '<tr>'
            + '<td class="element-row-cell"><span class="element-title">' + info.name + '</span></td>'
            + '<td class="letters-cell saad-cell">' + matrix.saad.join(' - ') + '</td>'
            + '<td class="letters-cell nahs-cell">' + matrix.nahs.join(' - ') + '</td>'
            + '</tr>';
    }

    html += '</tbody></table></div></div>';

    // Bottom section - Quran translation message + navigation tiles
    html += '<div class="verse-section navigate-section">';
    html += '<div class="toggle-section-title">استكشف القرآن مع الجمل</div>';
    html += '<p class="navigate-msg">لقد قمنا بترجمة القرآن الكريم كاملاً بقيم الجمل العددية، ونواصل إصدار السور حسب إتمامنا للمراجعة اللازمة. We have translated the entire Quran with Abjad numerical values and continue to roll out surahs as we complete our due diligence.</p>';
    html += '<div class="navigate-tiles">';
    html += '<a href="#" class="nav-tile" onclick="switchTab(\'surahs\'); return false;">';
    html += '<span class="nav-tile-icon">📜</span>';
    html += '<span class="nav-tile-title">السور</span>';
    html += '</a>';
    html += '<a href="#" class="nav-tile" onclick="switchTab(\'duas\'); return false;">';
    html += '<span class="nav-tile-icon">🤲</span>';
    html += '<span class="nav-tile-title">الأدعية</span>';
    html += '</a>';
    html += '<a href="#" class="nav-tile" onclick="switchTab(\'search\'); return false;">';
    html += '<span class="nav-tile-icon">🔍</span>';
    html += '<span class="nav-tile-title">البحث</span>';
    html += '</a>';
    html += '<a href="#" class="nav-tile" onclick="switchTab(\'calculator\'); return false;">';
    html += '<span class="nav-tile-icon">🧮</span>';
    html += '<span class="nav-tile-title">الحاسبة</span>';
    html += '</a>';
    html += '</div>';
    html += '</div>';

    html += '</div>';
    container.innerHTML = html;
}
