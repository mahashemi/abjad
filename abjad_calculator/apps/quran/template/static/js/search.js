// Quran Search Functionality
// Loads search index and provides multi-language search with Abjad values

let searchIndex = null;
let searchResults = [];

// Load search index from relative path
async function loadSearchIndex() {
  // Use relative path - works both locally and on GitHub Pages
  const indexUrl = 'abjad_calculator/apps/quran/template/static/data/quran_search_index.json';
  
  console.log('[SEARCH] Starting to load search index from:', indexUrl);
  
  try {
    console.log('[SEARCH] Fetching search index...');
    const response = await fetch(indexUrl);
    console.log('[SEARCH] Fetch response status:', response.status, response.statusText);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    console.log('[SEARCH] Parsing JSON...');
    searchIndex = await response.json();
    console.log('[SEARCH] ✓ Search index loaded successfully!');
    console.log('[SEARCH] Metadata:', searchIndex.metadata);
    console.log('[SEARCH] Total chapters:', searchIndex.chapters.length);
    console.log('[SEARCH] Total verses:', searchIndex.metadata.total_verses);
    console.log('[SEARCH] Languages:', searchIndex.metadata.languages);
    console.log('[SEARCH] Abjad systems:', searchIndex.metadata.abjad_systems);
    return true;
  } catch (error) {
    console.error('[SEARCH] ✗ Failed to load search index!');
    console.error('[SEARCH] Error details:', error);
    console.error('[SEARCH] URL attempted:', indexUrl);
    return false;
  }
}

// Render search interface
function renderSearchInterface() {
  console.log('[SEARCH] Rendering search interface...');
  const container = document.getElementById("surah-container");
  
  container.innerHTML = `
    <div class="search-section">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="ابحث في القرآن الكريم... Search the Quran..." />
        <button class="search-btn" onclick="performSearch()">بحث Search</button>
      </div>
      
      <button class="filters-toggle-btn" onclick="toggleFilters()">
        <span id="filtersToggleIcon">▼</span> خيارات البحث Advanced Filters
      </button>
      
      <div class="filters" id="searchFilters" style="display: none;">
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
  
  console.log('[SEARCH] Search parameters:');
  console.log('[SEARCH]   - Text:', searchText || '(none)');
  console.log('[SEARCH]   - Language:', language);
  console.log('[SEARCH]   - Abjad type:', abjadType || '(none)');
  console.log('[SEARCH]   - Chapter filter:', chapterFilter || 'All chapters');
  
  // Validate inputs
  if (!searchText && !abjadType) {
    console.warn('[SEARCH] ✗ No search criteria provided');
    alert('Please enter search text or select Abjad search');
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
  
  if (abjadType) {
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

// Text search in verses
function performTextSearch(chapters, searchText, language) {
  const searchLower = searchText.toLowerCase();
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      let matched = false;
      let matchedIn = [];
      
      // Search in specified language or all
      if (language === 'all' || language === 'arabic') {
        if (verse.arabic.includes(searchText) || verse.arabic.toLowerCase().includes(searchLower)) {
          matched = true;
          matchedIn.push('Arabic');
        }
      }
      if (language === 'all' || language === 'english') {
        if (verse.english.toLowerCase().includes(searchLower)) {
          matched = true;
          matchedIn.push('English');
        }
      }
      if (language === 'all' || language === 'urdu') {
        if (verse.urdu.includes(searchText) || verse.urdu.toLowerCase().includes(searchLower)) {
          matched = true;
          matchedIn.push('Urdu');
        }
      }
      if (language === 'all' || language === 'persian') {
        if (verse.persian.includes(searchText) || verse.persian.toLowerCase().includes(searchLower)) {
          matched = true;
          matchedIn.push('Persian');
        }
      }
      if (language === 'all' || language === 'transliteration') {
        if (verse.transliteration.toLowerCase().includes(searchLower)) {
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
          matchedIn: matchedIn
        });
      }
    });
  });
}

// Abjad value search
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
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      versesChecked++;
      const verseValue = verse.abjad[abjadType];
      if (verseValue >= minValue && verseValue <= maxValue) {
        console.log(`[SEARCH] ✓ Match found: Chapter ${chapter.chapter_number}:${verse.verse_number} = ${verseValue}`);
        searchResults.push({
          chapter: chapter.chapter_number,
          chapterName: chapter.chapter_name_arabic,
          verse: verse.verse_number,
          verseData: verse,
          abjadMatch: {
            type: abjadType,
            value: verseValue,
            target: targetValue
          }
        });
      }
    });
  });
  
  console.log('[SEARCH] Verses checked:', versesChecked);
  console.log('[SEARCH] Matches found:', searchResults.length);
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
  
  let html = `<h3 style="color: #d4af74; text-align: center; margin-bottom: 30px;">
    Found ${searchResults.length} results | تم العثور على ${searchResults.length} نتيجة
  </h3>`;
  
  searchResults.forEach(result => {
    const verse = result.verseData;
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
          <div class="result-arabic">${verse.arabic}</div>
          ${verse.english ? `<div class="result-translation" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>English:</strong> ${verse.english}</div>` : ''}
          ${verse.urdu ? `<div class="result-translation" dir="rtl" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>اردو:</strong> ${verse.urdu}</div>` : ''}
          ${verse.persian ? `<div class="result-translation" dir="rtl" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>فارسی:</strong> ${verse.persian}</div>` : ''}
          ${verse.transliteration ? `<div class="result-translation" style="padding-top: 10px; border-top: 1px solid rgba(143, 104, 26, 0.2);"><strong>Transliteration:</strong> ${verse.transliteration}</div>` : ''}
        </div>
        ${result.matchedIn ? `<div style="font-size: 14px; color: #5a3e2f; margin-top: 10px;">Matched in: ${result.matchedIn.join(', ')}</div>` : ''}
        ${result.abjadMatch ? `<div style="font-size: 14px; color: #2d7647; margin-top: 10px; font-weight: bold;">
          ${result.abjadMatch.type.charAt(0).toUpperCase() + result.abjadMatch.type.slice(1)}: ${result.abjadMatch.value} 
          (Target: ${result.abjadMatch.target})
        </div>` : ''}
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
