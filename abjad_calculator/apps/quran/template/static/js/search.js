// Quran Search Functionality
// Loads search index and provides multi-language search with Abjad values

let searchIndex = null;
let searchResults = [];

// Load search index from GitHub Pages
async function loadSearchIndex() {
  const USER = "mahashemi";
  const REPO = "abjad";
  const indexUrl = `https://${USER}.github.io/${REPO}/abjad_calculator/apps/quran/template/static/data/quran_search_index.json`;
  
  try {
    const response = await fetch(indexUrl);
    if (!response.ok) throw new Error('Failed to load search index');
    searchIndex = await response.json();
    console.log('Search index loaded:', searchIndex.metadata);
    return true;
  } catch (error) {
    console.error('Error loading search index:', error);
    return false;
  }
}

// Render search interface
function renderSearchInterface() {
  const container = document.getElementById("surah-container");
  
  container.innerHTML = `
    <div class="search-section">
      <div class="search-box">
        <input type="text" id="searchInput" placeholder="ابحث في القرآن الكريم... Search the Quran..." />
        <button class="search-btn" onclick="performSearch()">بحث Search</button>
      </div>
      
      <div class="filters">
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
    loadSearchIndex().then(success => {
      if (success) {
        populateChapterFilter();
      } else {
        document.getElementById('searchResults').innerHTML = 
          '<div class="error">Failed to load search index. Please refresh the page.</div>';
      }
    });
  } else {
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
  if (!searchIndex) return;
  
  const select = document.getElementById('chapterFilter');
  searchIndex.chapters.forEach(chapter => {
    const option = document.createElement('option');
    option.value = chapter.chapter_number;
    option.textContent = `سورة ${chapter.chapter_number}: ${chapter.chapter_name_arabic}`;
    select.appendChild(option);
  });
}

// Toggle abjad range input visibility
function toggleAbjadRange() {
  const abjadType = document.getElementById('abjadType').value;
  const rangeGroup = document.getElementById('abjadRangeGroup');
  rangeGroup.style.display = abjadType ? 'flex' : 'none';
}

// Perform search
function performSearch() {
  if (!searchIndex) {
    alert('Search index not loaded yet. Please wait...');
    return;
  }
  
  const searchText = document.getElementById('searchInput').value.trim();
  const language = document.getElementById('languageFilter').value;
  const abjadType = document.getElementById('abjadType').value;
  const chapterFilter = document.getElementById('chapterFilter').value;
  
  // Validate inputs
  if (!searchText && !abjadType) {
    alert('Please enter search text or select Abjad search');
    return;
  }
  
  searchResults = [];
  
  // Filter chapters if needed
  const chaptersToSearch = chapterFilter ? 
    [searchIndex.chapters.find(c => c.chapter_number == chapterFilter)] :
    searchIndex.chapters;
  
  // Perform search based on type
  if (abjadType) {
    performAbjadSearch(chaptersToSearch, abjadType);
  } else {
    performTextSearch(chaptersToSearch, searchText, language);
  }
  
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
function performAbjadSearch(chapters, abjadType) {
  const targetValue = parseInt(document.getElementById('abjadValue').value);
  const tolerance = parseInt(document.getElementById('abjadTolerance').value) || 0;
  
  if (isNaN(targetValue)) {
    alert('Please enter a valid Abjad value');
    return;
  }
  
  const minValue = targetValue - tolerance;
  const maxValue = targetValue + tolerance;
  
  chapters.forEach(chapter => {
    chapter.verses.forEach(verse => {
      const verseValue = verse.abjad[abjadType];
      if (verseValue >= minValue && verseValue <= maxValue) {
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
}

// Display search results
function displayResults() {
  const resultsDiv = document.getElementById('searchResults');
  
  if (searchResults.length === 0) {
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
          ${verse.english ? `<div class="result-translation"><strong>English:</strong> ${verse.english}</div>` : ''}
          ${verse.urdu ? `<div class="result-translation" dir="rtl"><strong>اردو:</strong> ${verse.urdu}</div>` : ''}
          ${verse.transliteration ? `<div class="result-translation"><strong>Transliteration:</strong> ${verse.transliteration}</div>` : ''}
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
}

// Make functions globally available
window.performSearch = performSearch;
window.toggleAbjadRange = toggleAbjadRange;
window.renderSearchInterface = renderSearchInterface;