// Quran Search Functionality
// Loads search index and provides multi-language search with Abjad values

let searchIndex = null;
let searchResults = [];

// Load search index from relative path
async function loadSearchIndex() {
  // Try multiple paths for local vs GitHub Pages compatibility
  const paths = [
    'abjad_calculator/apps/quran/template/static/data/quran_search_index.json', // GitHub Pages / deployed
  ];
  
  console.log('[SEARCH] Starting to load search index...');
  
  for (const indexUrl of paths) {
    try {
      console.log('[SEARCH] Trying path:', indexUrl);
      const response = await fetch(indexUrl);
      console.log('[SEARCH] Fetch response status:', response.status, response.statusText);
      
      if (!response.ok) {
        console.log('[SEARCH] Path failed, trying next...');
        continue;
      }
      
      console.log('[SEARCH] Parsing JSON...');
      searchIndex = await response.json();
      console.log('[SEARCH] ✓ Search index loaded successfully from:', indexUrl);
      console.log('[SEARCH] Metadata:', searchIndex.metadata);
      console.log('[SEARCH] Total chapters:', searchIndex.chapters.length);
      console.log('[SEARCH] Total verses:', searchIndex.metadata.total_verses);
      console.log('[SEARCH] Languages:', searchIndex.metadata.languages);
      console.log('[SEARCH] Abjad systems:', searchIndex.metadata.abjad_systems);
      return true;
    } catch (error) {
      console.log('[SEARCH] Error with path:', indexUrl, error.message);
    }
  }
  
  console.error('[SEARCH] ✗ Failed to load search index from all attempted paths!');
  console.error('[SEARCH] Paths attempted:', paths);
  return false;
}

// Render search interface
function renderSearchInterface() {
  console.log('[SEARCH] Rendering search interface...');
  const container = document.getElementById("surah-container");
  
  container.innerHTML = `
    <div class="search-section">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="ابحث في القرآن الكريم... Search the Quran..." />
      </div>
      
      <button class="filters-toggle-btn" onclick="toggleFilters()">
        <span id="filtersToggleIcon">▼</span> خيارات البحث Advanced Filters
      </button>
      
      <div class="filters" id="searchFilters" style="display: none;">
        <div class="filters-row">
          <div class="filter-group">
            <label>يبدأ بـ Starts With:</label>
            <input type="text" id="startsWithInput" placeholder="ابحث عن آيات تبدأ بـ..." />
          </div>
          
          <div class="filter-group">
            <label>ينتهي بـ Ends With:</label>
            <input type="text" id="endsWithInput" placeholder="ابحث عن آيات تنتهي بـ..." />
          </div>
        </div>
        
        <div class="filters-row">
          <div class="filter-group">
            <label>اللغة Language:</label>
            <select id="languageFilter">
              <option value="all">All جميع</option>
              <option value="arabic">العربية Arabic</option>
              <option value="english">English</option>
              <option value="urdu">اردو Urdu</option>
              <option value="persian">فارسی Persian</option>
              <option value="transliteration">Transliteration</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>البحث بالعدد Abjad Search:</label>
            <select id="abjadType" onchange="toggleAbjadRange()">
              <option value="">بحث نصي Text Only</option>
              <option value="qamari">القمري Qamari</option>
              <option value="malfuzi">الملفوظي Malfuzi</option>
              <option value="bayenati">الباطني Bayenati</option>
            </select>
          </div>
        </div>
        
        <div class="filter-group" id="abjadRangeGroup" style="display:none;">
          <label>القيمة Value:</label>
          <input type="number" id="abjadValue" placeholder="Value" style="width: 120px;">
          <span style="color: #d4af74;">±</span>
          <input type="number" id="abjadTolerance" placeholder="Tolerance" value="0" style="width: 80px;">
        </div>
        
        <div class="filter-group">
          <label>السورة Chapter:</label>
          <select id="chapterFilter">
            <option value="">جميع السور All</option>
          </select>
        </div>
      </div>
      
      <button class="search-btn" onclick="performSearch()" style="width: 100%; margin-top: 10px;">بحث Search</button>
      
      <div id="searchResults" class="search-results">
        <div class="welcome-search">
          <h2>مرحباً بكم في بحث القرآن الكريم</h2>
          <h2>Welcome to Quran Search</h2>
          <p>ابحث في القرآن الكريم بجميع اللغات المدعومة والأعداد الأبجدية</p>
          <p>Search the Holy Quran in all supported languages and Abjad values</p>
          <ul>
            <li>✓ بحث متعدد اللغات Multi-language search</li>
            <li>✓ البحث بالأعداد الأبجدية Search by Abjad numerical values</li>
            <li>✓ احصائيات على مستوى الآية Verse-level statistics</li>
            <li>✓ تحليل احرف وكلمات Letter and word analysis</li>
          </ul>
        </div>
      </div>
    </div>
  `;
  
  // Load search index if not loaded
  if (!searchIndex) {
    console.log('[SEARCH] Search index not loaded yet, loading now...');
    loadSearchIndex().then(success => {
      if (success) {
        console.log('[SEARCH] ✓ Search index loaded, populating chapter filter...');
        populateChapterFilter();
      } else {
        console.error('[SEARCH] ✗ Failed to load search index');
        document.getElementById('searchResults').innerHTML = 
          '<div class="error">Failed to load search index. Please refresh the page.</div>';
      }
    });
  } else {
    console.log('[SEARCH] ✓ Search index already loaded, populating chapter filter...');
    populateChapterFilter();
  }
  
  // Add enter key support for search
  document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      performSearch();
    }
  });
}

// Populate chapter filter dropdown
function populateChapterFilter() {
  if (!searchIndex) {
    console.warn('[SEARCH] Cannot populate chapter filter - search index not loaded');
    return;
  }
  
  console.log('[SEARCH] Populating chapter filter with', searchIndex.chapters.length, 'chapters...');
  const select = document.getElementById('chapterFilter');
  searchIndex.chapters.forEach(chapter => {
    const option = document.createElement('option');
    option.value = chapter.chapter_number;
    option.textContent = `سورة ${chapter.chapter_number}: ${chapter.chapter_name_arabic}`;
    select.appendChild(option);
  });
  console.log('[SEARCH] ✓ Chapter filter populated');
}

// Toggle abjad range input visibility
function toggleAbjadRange() {
  const abjadType = document.getElementById('abjadType').value;
  const rangeGroup = document.getElementById('abjadRangeGroup');
  rangeGroup.style.display = abjadType ? 'flex' : 'none';
}

// Perform search
function performSearch() {
  console.log('[SEARCH] ═══════════════════════════════════════');
  console.log('[SEARCH] Starting search...');
  
  if (!searchIndex) {
    console.error('[SEARCH] ✗ Search index not loaded!');
    alert('Search index not loaded yet. Please wait...');
    return;
  }
  
  const searchText = document.getElementById('searchInput').value.trim();
  const language = document.getElementById('languageFilter').value;
  const abjadType = document.getElementById('abjadType').value;
  const chapterFilter = document.getElementById('chapterFilter').value;
  const startsWithText = document.getElementById('startsWithInput').value.trim();
  const endsWithText = document.getElementById('endsWithInput').value.trim();
  
  console.log('[SEARCH] Search parameters:');
  console.log('[SEARCH]   - Text:', searchText || '(none)');
  console.log('[SEARCH]   - Starts With:', startsWithText || '(none)');
  console.log('[SEARCH]   - Ends With:', endsWithText || '(none)');
  console.log('[SEARCH]   - Language:', language);
  console.log('[SEARCH]   - Abjad type:', abjadType || '(none)');
  console.log('[SEARCH]   - Chapter filter:', chapterFilter || 'All chapters');
  
  // Validate inputs
  if (!searchText && !abjadType && !startsWithText && !endsWithText) {
    console.warn('[SEARCH] ✗ No search criteria provided');
    alert('Please enter search text, starts/ends with pattern, or select Abjad search');
    return;
  }
  
  searchResults = [];
  
  // Filter chapters if needed
  const chaptersToSearch = chapterFilter ? 
    [searchIndex.chapters.find(c => c.chapter_number == chapterFilter)] :
    searchIndex.chapters;
  
  console.log('[SEARCH] Chapters to search:', chaptersToSearch.length);
  
  // Smart search: If search text is a number and no Abjad type selected, search all Abjad systems
  const isNumericSearch = searchText && !isNaN(searchText) && searchText.trim() !== '';
  
  if (startsWithText || endsWithText) {
    // Pattern matching search (starts with / ends with)
    console.log('[SEARCH] Performing pattern matching search...');
    performPatternSearch(chaptersToSearch, startsWithText, endsWithText, language);
  } else if (abjadType) {
    // Explicit Abjad search with selected type
    console.log('[SEARCH] Performing Abjad search with type:', abjadType);
    performAbjadSearch(chaptersToSearch, abjadType);
  } else if (isNumericSearch) {
    // Auto-detect numeric search - search ALL Abjad systems
    console.log('[SEARCH] Detected numeric search, searching ALL Abjad systems for:', searchText);
    const targetValue = parseInt(searchText);
    performAbjadSearch(chaptersToSearch, 'qamari', targetValue);
    performAbjadSearch(chaptersToSearch, 'malfuzi', targetValue);
    performAbjadSearch(chaptersToSearch, 'bayenati', targetValue);
  } else {
    // Regular text search
    console.log('[SEARCH] Performing text search...');
    performTextSearch(chaptersToSearch, searchText, language);
  }
  
  console.log('[SEARCH] Search complete. Results found:', searchResults.length);
  displayResults();
}

// Text search in verses - supports word-level search using cleaned Arabic
function performTextSearch(chapters, searchText, language) {
  const searchLower = searchText.toLowerCase();
  
  // Split search text into individual words for word-level matching
  const searchWords = searchText.trim().split(/\s+/).filter(word => word.length > 0);
  
  console.log('[SEARCH] Word-level text search for', searchWords.length, 'word(s):', searchWords);
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      let matched = false;
      let matchedIn = [];
      let matchedWords = [];
      
      // Helper function to check if text matches search phrase
      const textMatches = (text, caseSensitive = false) => {
        if (!text) return false;
        
        const textToSearch = caseSensitive ? text : text.toLowerCase();
        const searchToUse = caseSensitive ? searchText : searchLower;
        
        // Match exact phrase in the sentence using includes
        return textToSearch.includes(searchToUse);
      };
      
      // Helper function for Arabic word-level search using word data
      const arabicWordMatches = () => {
        if (!verse.words || verse.words.length === 0) {
          // Fallback to simple text matching if word data not available
          return textMatches(verse.arabic_clean || verse.arabic);
        }
        
        // Check if search phrase exists in cleaned text and populate matched words
        if (verse.arabic_clean && verse.arabic_clean.includes(searchText)) {
          // Find which words contain the search text
          verse.words.forEach(wordData => {
            if (wordData.word.includes(searchText) && !matchedWords.includes(wordData.word)) {
              matchedWords.push(wordData.word);
            }
          });
          return true;
        }
        
        // Word-level search: check if all search words match any word in verse
        const allWordsMatch = searchWords.every(searchWord => {
          return verse.words.some(wordData => {
            const matches = wordData.word.includes(searchWord);
            if (matches && !matchedWords.includes(wordData.word)) {
              matchedWords.push(wordData.word);
            }
            return matches;
          });
        });
        
        return allWordsMatch;
      };
      
      // Search in specified language or all
      if (language === 'all' || language === 'arabic') {
        if (arabicWordMatches()) {
          matched = true;
          matchedIn.push('Arabic');
        }
      }
      if (language === 'all' || language === 'english') {
        if (textMatches(verse.english)) {
          matched = true;
          matchedIn.push('English');
        }
      }
      if (language === 'all' || language === 'urdu') {
        if (textMatches(verse.urdu, true) || textMatches(verse.urdu, false)) {
          matched = true;
          matchedIn.push('Urdu');
        }
      }
      if (language === 'all' || language === 'persian') {
        if (textMatches(verse.persian, true) || textMatches(verse.persian, false)) {
          matched = true;
          matchedIn.push('Persian');
        }
      }
      if (language === 'all' || language === 'transliteration') {
        if (textMatches(verse.transliteration)) {
          matched = true;
          matchedIn.push('Transliteration');
        }
      }
      
      if (matched) {
        searchResults.push({
          chapter: chapter.chapter_number,
          chapterName: chapter.chapter_name_arabic,
          verse: verse.verse_number,
          verseData: verse,
          matchedIn: matchedIn,
          matchedWords: matchedWords  // Store matched words for display
        });
      }
    });
  });
  
  console.log('[SEARCH] Word-level text search complete. Found', searchResults.length, 'verses');
}

// Pattern matching search for verses that start with or end with specific text
function performPatternSearch(chapters, startsWithText, endsWithText, language) {
  console.log('[SEARCH] Pattern search parameters:');
  console.log('[SEARCH]   - Starts with:', startsWithText || '(none)');
  console.log('[SEARCH]   - Ends with:', endsWithText || '(none)');
  console.log('[SEARCH]   - Language:', language);
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      let matched = false;
      let matchedIn = [];
      let patternInfo = { startsWith: false, endsWith: false };
      
      // Helper function to check if text starts with pattern
      const checkStartsWith = (text) => {
        if (!text || !startsWithText) return false;
        return text.trimStart().startsWith(startsWithText);
      };
      
      // Helper function to check if text ends with pattern
      const checkEndsWith = (text) => {
        if (!text || !endsWithText) return false;
        return text.trimEnd().endsWith(endsWithText);
      };
      
      // Check conditions based on what was provided
      const needsStartsWith = startsWithText.length > 0;
      const needsEndsWith = endsWithText.length > 0;
      
      // Pattern search only works with Arabic and Transliteration
      if (language === 'all' || language === 'arabic') {
        const text = verse.arabic_clean || verse.arabic;
        const startsMatch = !needsStartsWith || checkStartsWith(text);
        const endsMatch = !needsEndsWith || checkEndsWith(text);
        
        if (startsMatch && endsMatch) {
          matched = true;
          matchedIn.push('Arabic');
          if (needsStartsWith && checkStartsWith(text)) patternInfo.startsWith = true;
          if (needsEndsWith && checkEndsWith(text)) patternInfo.endsWith = true;
        }
      }
      if (language === 'all' || language === 'transliteration') {
        const text = verse.transliteration;
        const startsMatch = !needsStartsWith || checkStartsWith(text);
        const endsMatch = !needsEndsWith || checkEndsWith(text);
        
        if (startsMatch && endsMatch) {
          matched = true;
          matchedIn.push('Transliteration');
          if (needsStartsWith && checkStartsWith(text)) patternInfo.startsWith = true;
          if (needsEndsWith && checkEndsWith(text)) patternInfo.endsWith = true;
        }
      }
      
      if (matched) {
        searchResults.push({
          chapter: chapter.chapter_number,
          chapterName: chapter.chapter_name_arabic,
          verse: verse.verse_number,
          verseData: verse,
          matchedIn: matchedIn,
          patternMatch: {
            startsWith: startsWithText,
            endsWith: endsWithText,
            matchInfo: patternInfo
          }
        });
      }
    });
  });
  
  console.log('[SEARCH] Pattern matching search complete. Found', searchResults.length, 'verses');
}

// Abjad value search - supports both verse-level and word-level matching
function performAbjadSearch(chapters, abjadType, manualValue = null) {
  const targetValue = manualValue !== null ? manualValue : parseInt(document.getElementById('abjadValue').value);
  const tolerance = manualValue !== null ? 0 : (parseInt(document.getElementById('abjadTolerance').value) || 0);
  
  console.log('[SEARCH] Abjad search parameters:');
  console.log('[SEARCH]   - Type:', abjadType);
  console.log('[SEARCH]   - Target value:', targetValue);
  console.log('[SEARCH]   - Tolerance:', tolerance);
  
  if (isNaN(targetValue)) {
    console.error('[SEARCH] ✗ Invalid Abjad value');
    alert('Please enter a valid Abjad value');
    return;
  }
  
  const minValue = targetValue - tolerance;
  const maxValue = targetValue + tolerance;
  console.log('[SEARCH]   - Search range:', minValue, 'to', maxValue);
  
  let versesChecked = 0;
  let wordMatches = 0;
  let verseMatches = 0;
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      versesChecked++;
      let matched = false;
      let matchType = null;
      let matchedWords = [];
      
      // First check verse-level match
      const verseValue = verse.abjad[abjadType];
      if (verseValue >= minValue && verseValue <= maxValue) {
        matched = true;
        matchType = 'verse';
        verseMatches++;
        console.log(`[SEARCH] ✓ Verse match: Chapter ${chapter.chapter_number}:${verse.verse_number} = ${verseValue}`);
      }
      
      // Then check word-level matches (if verse has word data)
      if (verse.words && verse.words.length > 0) {
        verse.words.forEach(wordData => {
          const wordValue = wordData[abjadType];
          if (wordValue >= minValue && wordValue <= maxValue) {
            matched = true;
            if (matchType !== 'verse') {
              matchType = 'word';
            }
            matchedWords.push({
              word: wordData.word,
              position: wordData.position,
              value: wordValue
            });
          }
        });
        
        if (matchedWords.length > 0 && matchType === 'word') {
          wordMatches++;
          console.log(`[SEARCH] ✓ Word match: Chapter ${chapter.chapter_number}:${verse.verse_number} - ${matchedWords.length} word(s) matched`);
        }
      }
      
      if (matched) {
        // Check if this verse was already added (to avoid duplicates)
        const alreadyExists = searchResults.some(r => 
          r.chapter === chapter.chapter_number && 
          r.verse === verse.verse_number &&
          r.abjadMatch && 
          r.abjadMatch.type === abjadType
        );
        
        if (!alreadyExists) {
          searchResults.push({
            chapter: chapter.chapter_number,
            chapterName: chapter.chapter_name_arabic,
            verse: verse.verse_number,
            verseData: verse,
            abjadMatch: {
              type: abjadType,
              value: verseValue,
              target: targetValue,
              matchType: matchType,
              matchedWords: matchedWords  // Store matched words with their values
            }
          });
        }
      }
    });
  });
  
  console.log('[SEARCH] Verses checked:', versesChecked);
  console.log('[SEARCH] Verse-level matches:', verseMatches);
  console.log('[SEARCH] Word-level matches:', wordMatches);
  console.log('[SEARCH] Total unique verses found:', searchResults.filter(r => r.abjadMatch && r.abjadMatch.type === abjadType).length);
}

// Helper function to highlight Arabic text by mapping cleaned text indices to original with harakats
function highlightArabicByIndex(arabicOriginal, arabicClean, searchText, isNumeric = false) {
  if (!arabicOriginal || !arabicClean || !searchText) return arabicOriginal;
  
  const highlightStyle = isNumeric 
    ? 'text-decoration: underline; text-decoration-color: #2d7647; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold;'
    : 'text-decoration: underline; text-decoration-color: #d4af74; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold;';
  
  // Find all occurrences of search phrase in cleaned text
  const searchLower = searchText.toLowerCase();
  const cleanLower = arabicClean.toLowerCase();
  
  let result = arabicOriginal;
  const matches = [];
  let startIndex = 0;
  
  // Find all match positions in cleaned text
  while ((startIndex = cleanLower.indexOf(searchLower, startIndex)) !== -1) {
    matches.push({
      cleanStart: startIndex,
      cleanEnd: startIndex + searchText.length
    });
    startIndex += searchText.length;
  }
  
  if (matches.length === 0) {
    return arabicOriginal;
  }
  
  // Match Python's clean_text() function which uses:
  // 1. REMOVE_CHARS list (with .strip() applied to each char)
  // 2. strip_diacritics() regex: [\u064B-\u065F\u0670]
  const isRemovedChar = (char) => {
    // strip_diacritics regex: U+064B to U+065F and U+0670
    if (char >= '\u064B' && char <= '\u065F') return true;
    if (char === '\u0670') return true;
    
    // REMOVE_CHARS from constants.py (trimmed)
    const removeChars = [
      // Tashkeel (also covered by regex above but listed for completeness)
      'ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ',
      // Quranic diacritics
      'ٓ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۝', '۞',
      '۟', '۠', 'ۡ', 'ۢ', 'ۣ', 'ۤ', 'ۥ', 'ۦ', 'ۧ', 'ۨ',
      '۩', '۪', '۫', '۬', 'ۭ', 'ٗ',
      // Hamza standalone
      'ء',
      // Whitespace and control (note: space ' ' between words is NOT removed in cleaned text)
      '\n', '\t', '\r', '\u200c', '\u200d', '\u202c'
    ];
    
    return removeChars.includes(char);
  };
  
  // Build a mapping from cleaned indices to original indices
  const indexMap = [];
  let cleanIdx = 0;
  
  console.log('[HIGHLIGHT] Building index map...');
  console.log('[HIGHLIGHT] Original length:', arabicOriginal.length);
  console.log('[HIGHLIGHT] Cleaned length:', arabicClean.length);
  
  for (let origIdx = 0; origIdx < arabicOriginal.length; origIdx++) {
    const char = arabicOriginal[origIdx];
    const charCode = char.charCodeAt(0).toString(16);
    
    // Skip characters that are removed during cleaning
    if (isRemovedChar(char)) {
      console.log(`[HIGHLIGHT] Skipping removed char at orig[${origIdx}]: "${char}" (U+${charCode})`);
      continue;
    }
    
    // Check if this character exists in cleaned text at current position
    if (cleanIdx < arabicClean.length && arabicClean[cleanIdx] === char) {
      indexMap[cleanIdx] = origIdx;
      console.log(`[HIGHLIGHT] Mapped clean[${cleanIdx}] = orig[${origIdx}]: "${char}"`);
      cleanIdx++;
    } else {
      console.log(`[HIGHLIGHT] Mismatch at orig[${origIdx}]: "${char}" (U+${charCode}), expected clean[${cleanIdx}]: "${arabicClean[cleanIdx] || 'EOF'}"`);
    }
  }
  // Add final mapping for end of string
  indexMap[cleanIdx] = arabicOriginal.length;
  
  console.log('[HIGHLIGHT] Index map complete. Mapped', cleanIdx, 'clean chars to', arabicOriginal.length, 'original chars');
  
  // Apply highlights from end to start to avoid index shifting
  matches.reverse().forEach(match => {
    const origStart = indexMap[match.cleanStart] || 0;
    const origEnd = indexMap[match.cleanEnd] || arabicOriginal.length;
    
    const before = result.substring(0, origStart);
    const highlighted = result.substring(origStart, origEnd);
    const after = result.substring(origEnd);
    
    result = before + `<mark style="${highlightStyle}">${highlighted}</mark>` + after;
  });
  
  return result;
}

// Helper function to highlight matched phrase in text
function highlightText(text, searchText, isNumeric = false) {
  if (!text || !searchText) return text;
  
  const highlightStyle = isNumeric 
    ? 'background: rgba(45, 118, 71, 0.3); padding: 2px 4px; border-radius: 3px; font-weight: bold;'
    : 'background: rgba(212, 175, 116, 0.4); padding: 2px 4px; border-radius: 3px;';
  
  // Escape special regex characters in the search phrase
  const escapedPhrase = searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  // Create case-insensitive regex to find the exact phrase
  const regex = new RegExp(`(${escapedPhrase})`, 'gi');
  
  // Replace all occurrences of the phrase with highlighted version
  return text.replace(regex, `<mark style="${highlightStyle}">$1</mark>`);
}

// Helper function to highlight specific words by position mapping
function highlightWordsByPosition(arabicText, arabicClean, matchedWords, allWords, isNumeric = false) {
  if (!arabicText || !matchedWords || matchedWords.length === 0) return arabicText;
  
  const highlightStyle = isNumeric 
    ? 'text-decoration: underline; text-decoration-color: #2d7647; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold; cursor: help;'
    : 'text-decoration: underline; text-decoration-color: #d4af74; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold; cursor: help;';
  
  // Build a map of positions to word data (including abjad values)
  const positionToWordData = new Map();
  matchedWords.forEach(matchedWord => {
    if (allWords && allWords.length > 0) {
      allWords.forEach(wordData => {
        if (wordData.word === matchedWord) {
          positionToWordData.set(wordData.position, wordData);
        }
      });
    }
  });
  
  if (positionToWordData.size === 0) {
    // Fallback to simple string matching if no positions found
    return highlightSpecificWords(arabicText, matchedWords, isNumeric);
  }
  
  // Split original Arabic text by spaces to get words with harakats
  const originalWords = arabicText.trim().split(/\s+/);
  
  // Highlight words at matched positions with abjad values in tooltip
  const highlightedWords = originalWords.map((word, index) => {
    const position = index + 1; // Positions are 1-indexed
    const wordData = positionToWordData.get(position);
    
    if (wordData) {
      // Build tooltip with abjad values
      const tooltip = `القمري: ${wordData.qamari} | الملفوظي: ${wordData.malfuzi} | الباطني: ${wordData.bayenati}`;
      return `<mark style="${highlightStyle}" title="${tooltip}">${word}</mark>`;
    }
    return word;
  });
  
  return highlightedWords.join(' ');
}

// Helper function to highlight specific words by exact match (fallback)
function highlightSpecificWords(text, wordsArray, isNumeric = false) {
  if (!text || !wordsArray || wordsArray.length === 0) return text;
  
  const highlightStyle = isNumeric 
    ? 'text-decoration: underline; text-decoration-color: #2d7647; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold;'
    : 'text-decoration: underline; text-decoration-color: #d4af74; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold;';
  
  let highlightedText = text;
  
  // Sort by length (longest first) to avoid partial matches
  const sortedWords = [...wordsArray].sort((a, b) => b.length - a.length);
  
  sortedWords.forEach(word => {
    // Escape special regex characters
    const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedWord})`, 'g');
    highlightedText = highlightedText.replace(regex, `<mark style="${highlightStyle}">$1</mark>`);
  });
  
  return highlightedText;
}

// Helper function to highlight pattern matches (starts/ends with)
function highlightPatternMatch(text, startsWithText, endsWithText) {
  if (!text) return text;
  
  let result = text;
  const highlightStyle = 'text-decoration: underline; text-decoration-color: #b48a1f; text-decoration-thickness: 2px; text-underline-offset: 2px; font-weight: bold;';
  
  // Highlight start pattern
  if (startsWithText) {
    const trimmedText = text.trimStart();
    const leadingSpaces = text.length - trimmedText.length;
    const spaces = text.substring(0, leadingSpaces);
    
    if (trimmedText.startsWith(startsWithText)) {
      const highlighted = `<mark style="${highlightStyle}">${startsWithText}</mark>`;
      const rest = trimmedText.substring(startsWithText.length);
      result = spaces + highlighted + rest;
    }
  }
  
  // Highlight end pattern
  if (endsWithText) {
    const trimmedText = result.trimEnd();
    const trailingSpaces = result.length - trimmedText.length;
    const spaces = result.substring(trimmedText.length);
    
    if (trimmedText.endsWith(endsWithText)) {
      const startIdx = trimmedText.lastIndexOf(endsWithText);
      const before = trimmedText.substring(0, startIdx);
      const highlighted = `<mark style="${highlightStyle}">${endsWithText}</mark>`;
      result = before + highlighted + spaces;
    }
  }
  
  return result;
}

// Display search results
function displayResults() {
  console.log('[SEARCH] Displaying', searchResults.length, 'results...');
  const resultsDiv = document.getElementById('searchResults');
  
  if (searchResults.length === 0) {
    console.log('[SEARCH] No results to display');
    resultsDiv.innerHTML = `
      <div class="error">
        No results found. لم يتم العثور على نتائج
      </div>
    `;
    return;
  }
  
  // Get the search text from input for highlighting
  const searchText = document.getElementById('searchInput').value.trim();
  const startsWithText = document.getElementById('startsWithInput').value.trim();
  const endsWithText = document.getElementById('endsWithInput').value.trim();
  
  let html = `<h3 style="color: #d4af74; text-align: center; margin-bottom: 30px;">
    Found ${searchResults.length} results | تم العثور على ${searchResults.length} نتيجة
  </h3>`;
  
  searchResults.forEach(result => {
    const verse = result.verseData;
    
    // Prepare text for each language with highlighting
    let arabicText = verse.arabic;
    let englishText = verse.english;
    let urduText = verse.urdu;
    let persianText = verse.persian;
    let translitText = verse.transliteration;
    
    // Apply highlighting based on match type - can apply multiple types
    
    // 1. Pattern matching (starts/ends with) - bronze highlight
    if (result.patternMatch) {
      if (result.matchedIn && result.matchedIn.includes('Arabic')) {
        const textToHighlight = verse.arabic_clean || verse.arabic;
        arabicText = highlightPatternMatch(arabicText, 
          result.patternMatch.matchInfo.startsWith ? result.patternMatch.startsWith : null,
          result.patternMatch.matchInfo.endsWith ? result.patternMatch.endsWith : null);
      }
      
      // Apply pattern highlighting to other languages
      if (result.matchedIn) {
        if (result.matchedIn.includes('English') && englishText) {
          englishText = highlightPatternMatch(englishText,
            result.patternMatch.matchInfo.startsWith ? result.patternMatch.startsWith : null,
            result.patternMatch.matchInfo.endsWith ? result.patternMatch.endsWith : null);
        }
        if (result.matchedIn.includes('Urdu') && urduText) {
          urduText = highlightPatternMatch(urduText,
            result.patternMatch.matchInfo.startsWith ? result.patternMatch.startsWith : null,
            result.patternMatch.matchInfo.endsWith ? result.patternMatch.endsWith : null);
        }
        if (result.matchedIn.includes('Persian') && persianText) {
          persianText = highlightPatternMatch(persianText,
            result.patternMatch.matchInfo.startsWith ? result.patternMatch.startsWith : null,
            result.patternMatch.matchInfo.endsWith ? result.patternMatch.endsWith : null);
        }
        if (result.matchedIn.includes('Transliteration') && translitText) {
          translitText = highlightPatternMatch(translitText,
            result.patternMatch.matchInfo.startsWith ? result.patternMatch.startsWith : null,
            result.patternMatch.matchInfo.endsWith ? result.patternMatch.endsWith : null);
        }
      }
    }
    
    // 2. Numeric word-level matches (green highlight with tooltips)
    if (result.abjadMatch && result.abjadMatch.matchType === 'word' && result.abjadMatch.matchedWords) {
      const matchedWordTexts = result.abjadMatch.matchedWords.map(w => w.word);
      arabicText = highlightWordsByPosition(arabicText, verse.arabic_clean, matchedWordTexts, verse.words, true);
    }
    
    // 3. Text search word matches (golden highlight with tooltips)
    // Apply word-level highlighting for text searches that have matched words
    if (result.matchedWords && result.matchedWords.length > 0) {
      arabicText = highlightWordsByPosition(arabicText, verse.arabic_clean, result.matchedWords, verse.words, false);
    } 
    // 4. Text search phrase matches (golden highlight) - fallback for phrase-only matches
    else if (result.matchedIn && searchText && result.matchedIn.includes('Arabic')) {
      // Apply phrase highlighting only if no word matches
      arabicText = highlightArabicByIndex(arabicText, verse.arabic_clean, searchText, false);
    }
    
    // Apply highlighting to other languages (for text search only)
    if (result.matchedIn && searchText && !result.patternMatch) {
      if (result.matchedIn.includes('English') && englishText) {
        englishText = highlightText(englishText, searchText, false);
      }
      if (result.matchedIn.includes('Urdu') && urduText) {
        urduText = highlightText(urduText, searchText, false);
      }
      if (result.matchedIn.includes('Persian') && persianText) {
        persianText = highlightText(persianText, searchText, false);
      }
      if (result.matchedIn.includes('Transliteration') && translitText) {
        translitText = highlightText(translitText, searchText, false);
      }
    }
    
    // Build match info
    let matchInfo = '';
    
    // Pattern match info
    if (result.patternMatch) {
      let patternDesc = [];
      if (result.patternMatch.matchInfo.startsWith) {
        patternDesc.push(`Starts with: "${result.patternMatch.startsWith}"`);
      }
      if (result.patternMatch.matchInfo.endsWith) {
        patternDesc.push(`Ends with: "${result.patternMatch.endsWith}"`);
      }
      
      if (patternDesc.length > 0) {
        matchInfo += `<div style="font-size: 13px; color: #b4881f; margin-top: 8px; font-weight: bold;">
          ✓ Pattern Match: ${patternDesc.join(' AND ')}
        </div>`;
      }
    }
    
    // Abjad match info
    if (result.abjadMatch) {
      const abjadType = result.abjadMatch.type;
      const abjadTypeLabel = abjadType.charAt(0).toUpperCase() + abjadType.slice(1);
      
      if (result.abjadMatch.matchType === 'verse') {
        matchInfo += `<div style="font-size: 13px; color: #2d7647; margin-top: 8px; font-weight: bold;">
          ✓ Verse Match: ${abjadTypeLabel} = ${result.abjadMatch.value} (Target: ${result.abjadMatch.target})
        </div>`;
      } else if (result.abjadMatch.matchType === 'word' && result.abjadMatch.matchedWords) {
        const wordsInfo = result.abjadMatch.matchedWords
          .map(w => `${w.word} (${w.value})`)
          .join(' • ');
        matchInfo += `<div style="font-size: 13px; color: #2d7647; margin-top: 8px;">
          <strong>✓ ${result.abjadMatch.matchedWords.length} word(s) matched in ${abjadTypeLabel}:</strong> ${wordsInfo}
        </div>`;
      }
    }
    
    html += `
      <div class="result-item">
        <div class="result-header">
          <div class="result-reference">
            سورة ${result.chapter}: ${result.chapterName} - آية ${result.verse}
          </div>
          <div class="result-abjad">
            <span>القمري: ${verse.abjad.qamari}</span>
            <span>الملفوظي: ${verse.abjad.malfuzi}</span>
            <span>الباطني: ${verse.abjad.bayenati}</span>
          </div>
        </div>
        <div class="result-text">
          <div class="result-arabic">${arabicText}</div>
          ${englishText ? `<div class="result-translation" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>English:</strong> ${englishText}</div>` : ''}
          ${urduText ? `<div class="result-translation" dir="rtl" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>اردو:</strong> ${urduText}</div>` : ''}
          ${persianText ? `<div class="result-translation" dir="rtl" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>فارسی:</strong> ${persianText}</div>` : ''}
          ${translitText ? `<div class="result-translation" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>Transliteration:</strong> ${translitText}</div>` : ''}
        </div>
        ${result.matchedIn ? `<div style="font-size: 14px; color: #5a3e2f; margin-top: 10px;">Matched in: ${result.matchedIn.join(', ')}</div>` : ''}
        ${matchInfo}
      </div>
    `;
  });
  
  resultsDiv.innerHTML = html;
  console.log('[SEARCH] ✓ Results displayed successfully');
  console.log('[SEARCH] ═══════════════════════════════════════');
}

// Toggle filters visibility
function toggleFilters() {
  const filters = document.getElementById('searchFilters');
  const icon = document.getElementById('filtersToggleIcon');
  
  if (filters.style.display === 'none') {
    filters.style.display = 'flex';
    icon.textContent = '▲';
  } else {
    filters.style.display = 'none';
    icon.textContent = '▼';
  }
}

// Make functions globally available
window.performSearch = performSearch;
window.toggleAbjadRange = toggleAbjadRange;
window.renderSearchInterface = renderSearchInterface;
window.toggleFilters = toggleFilters;
