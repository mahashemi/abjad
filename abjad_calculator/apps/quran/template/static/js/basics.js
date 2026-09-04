/**
 * Basics Page - Educational Tables
 * Reuses Quran surah page design patterns
 */
 * Constants loaded from abjad-constants.js

function renderBasicsPage(container) {
    let html = '<div class="container basics-container">';

    // Page header (like surah_header)
    html += '<div class="surah_header surah_name container arabic-font">';
    html += '<div class="surat-name-value name-elements">أساسيات حساب الجمل</div>';
    html += '<div class="surat-number-value name-elements" style="font-size:16px;">Abjad Numerical System</div>';
    html += '</div>';

    // Section 1: Qamari Table (static cards - no click)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">📊 جدول القمري (Qamari Values)</div>';
    html += '<div class="word-cards-row">';

    const qamariGroups = {};
    const allLetters = ["ا", "أ", "ٱ", "إ", "آ", "ب", "پ", "ج", "چ", "د", "ه", "ة", "ہ", "ھ", "و", "ؤ", "ز", "ژ", "ح", "ط", "ي", "ى", "ی", "ئ", "ك", "ک", "گ", "ل", "م", "ن", "س", "ع", "ف", "ص", "ق", "ر", "ڑ", "ش", "ت", "ٹ", "ث", "خ", "ذ", "ض", "ظ", "غ"];

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
        html += '<div class="word-values"><span class="value-qamari">' + qamari + '</span></div>';
        html += '</div>';
    }

    html += '</div></div>';

    // Section 2: Malfuzi Table (click to expand - like Quran word cards)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">📊 جدول الملفوظي (Malfuzi Values)</div>';
    html += '<div class="word-cards-row">';

    const malfuziGroups = {};
    for (const letter of allLetters) {
        const data = ABJAD_VALUES[letter];
        if (data) {
            const key = data.malfuzi;
            if (!malfuziGroups[key]) {
                malfuziGroups[key] = { letters: [], name: data.name, nameBreakdown: calculateAbjad(data.name) };
            }
            malfuziGroups[key].letters.push(letter);
        }
    }

    const sortedMalfuziKeys = Object.keys(malfuziGroups).sort((a, b) => parseInt(a) - parseInt(b));
    for (const malfuzi of sortedMalfuziKeys) {
        const group = malfuziGroups[malfuzi];
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
        html += '<div class="word-values"><span class="value-malfuzi">' + malfuzi + '</span></div>';
        html += '</div>';
    }

    html += '</div></div>';

    // Section 3: Elements x Nature Table (element on right)
    html += '<div class="verse-section">';
    html += '<div class="toggle-section-title">🌍 العناصر والطبائع (Elements & Nature)</div>';
    html += '<div class="table-wrapper"><table class="basics-table element-table">';
    html += '<thead><tr><th>سعد<br><small>Saad</small></th><th>نحس<br><small>Nahs</small></th><th>عُنْصُر<br><small>Element</small></th></tr></thead>';
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
        html += '<tr><td class="letters-cell saad-cell">' + matrix.saad.join('، ') + '</td><td class="letters-cell nahs-cell">' + matrix.nahs.join('، ') + '</td><td class="element-row-cell"><span class="element-icon">' + info.icon + '</span> ' + info.name + '<br><small>' + info.meaning + '</small></td></tr>';
    }

    html += '</tbody></table></div></div>';

    html += '</div>';
    container.innerHTML = html;
}
