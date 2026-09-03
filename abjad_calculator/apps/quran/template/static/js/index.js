const USER = "mahashemi"; // ← your GitHub user/org
const REPO = "abjad"; // ← your repo name
const QURAN_FOLDER = "output/quran"; // ← path under repo root for quran
const DUAS_FOLDER = "output/duas"; // ← path under repo root for duas

let allFiles = []; // Store all files for filtering
let currentTab = 'surahs'; // Track current active tab

let calculatorLoaded = false;

function switchTab(tabName) {
  currentTab = tabName;

  // Update button states - be specific to target only .tab-button
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.remove('active');
  });
  // Specifically target .tab-button, not mobile menu items
  const targetButton = document.querySelector(`.tab-button[data-tab="${tabName}"]`);
  if (targetButton) {
    targetButton.classList.add('active');
  }

  // Handle different tabs
  if (tabName === 'search') {
    renderSearchInterface();
  } else if (tabName === 'calculator') {
    showCalculator();
  } else {
    renderFiles(allFiles, tabName);
  }
}

function renderFiles(files, filterTab = 'surahs') {
  const container = document.getElementById("surah-container");
  container.innerHTML = "";

  const htmlFiles = files
    .filter((f) => f.name.toLowerCase().endsWith(".html"))
    .map((f) => {
      var match = f.name.match(/سورة\s(\d+)/); // e.g., سورة 103
      const isDua = match === null;
      if (isDua)
        match = f.name.match(/دُعَاءُ\s(\d+)/); // e.g., دُعَاءُ 1
      const surahNum = match ? parseInt(match[1], 10) : 0;
      return { ...f, surahNum, isDua };
    })
    .filter((f) => {
      // Filter based on active tab
      if (filterTab === 'surahs') {
        return !f.isDua;
      } else {
        return f.isDua;
      }
    })
    .sort((a, b) => a.surahNum - b.surahNum); // sort by number

  htmlFiles.forEach((f) => {
    // Extract Arabic name from the filename
    var nameMatch = f.name.match(/سورة\s([^-]+)/);
    if (nameMatch === null)
      nameMatch = f.name.match(/دُعَاءُ\s([^-]+)/);
    const arabicName = nameMatch ? nameMatch[1].trim() : "";

    // Extract verse count if available
    var verseMatch = f.name.match(/عدد آياتها\s(\d+)/);
    if (verseMatch === null)
      verseMatch = f.name.match(/عدد سترها\s(\d+)/);
    const verseCount = verseMatch
      ? parseInt(verseMatch[1], 10)
      : null;

    // Determine the correct folder
    const folder = f.isDua ? DUAS_FOLDER : QURAN_FOLDER;

    // Create book element
    const bookLink = document.createElement("a");
    bookLink.className = "surah-book";
    bookLink.href = `https://${USER}.github.io/${REPO}/${folder}/${encodeURIComponent(
      f.name
    )}`;
    bookLink.target = "_blank";
    bookLink.rel = "noopener noreferrer";

    // Create number badge
    const numberBadge = document.createElement("span");
    numberBadge.className = "surah-number";
    numberBadge.textContent = f.isDua ? `دُعَاءُ ${f.surahNum}` : `سورة ${f.surahNum}`;

    // Create Arabic name element as the main central element
    const nameDiv = document.createElement("div");
    nameDiv.className = "surah-name";
    nameDiv.textContent = arabicName;

    // Add verse count if available (bottom right)
    if (verseCount) {
      const verseCountSpan = document.createElement("span");
      verseCountSpan.className = "verse-count";
      verseCountSpan.textContent = f.isDua ? ` عدد سترها ${verseCount}` : ` عدد آياتها ${verseCount}`;
      bookLink.appendChild(verseCountSpan);
    }

    // Assemble book element
    bookLink.appendChild(numberBadge);
    bookLink.appendChild(nameDiv);

    container.appendChild(bookLink);
  });

  // If no files found for this tab
  if (htmlFiles.length === 0) {
    const message = filterTab === 'surahs' ? 'لا توجد سور' : 'لا توجد أدعية';
    container.innerHTML = `<div class="error">${message}</div>`;
  }
}

// Fetch files from both folders
Promise.all([
  fetch(`https://api.github.com/repos/${USER}/${REPO}/contents/${QURAN_FOLDER}`)
    .then((r) => (r.ok ? r.json() : []))
    .catch(() => []),
  fetch(`https://api.github.com/repos/${USER}/${REPO}/contents/${DUAS_FOLDER}`)
    .then((r) => (r.ok ? r.json() : []))
    .catch(() => [])
])
  .then(([quranFiles, duaFiles]) => {
    allFiles = [...quranFiles, ...duaFiles]; // Combine files from both folders
    
    // Don't call switchTab - the HTML already has active class set
    // Just render the initial content for the current tab
    renderFiles(allFiles, currentTab);
  })
  .catch((err) => {
    document.getElementById(
      "surah-container"
    ).innerHTML = `<div class="error">Error loading files: ${err}</div>`;
  });

// Mobile menu functions
function toggleMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const overlay = document.getElementById('mobileMenuOverlay');
  const menu = document.getElementById('mobileMenu');
  
  btn.classList.toggle('active');
  overlay.classList.toggle('active');
  menu.classList.toggle('active');
}

function closeMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const overlay = document.getElementById('mobileMenuOverlay');
  const menu = document.getElementById('mobileMenu');
  
  btn.classList.remove('active');
  overlay.classList.remove('active');
  menu.classList.remove('active');
}

function switchTabMobile(tabName) {
  // Close mobile menu
  closeMobileMenu();

  // Update currentTab
  currentTab = tabName;

  // Update mobile menu item states
  document.querySelectorAll('.mobile-menu-item').forEach(item => {
    item.classList.remove('active');
  });
  document.querySelector(`.mobile-menu-item[data-tab="${tabName}"]`).classList.add('active');

  // Also update desktop tab button states to keep them in sync
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.remove('active');
  });
  const desktopTab = document.querySelector(`.tab-button[data-tab="${tabName}"]`);
  if (desktopTab) {
    desktopTab.classList.add('active');
  }

  // Handle different tabs
  if (tabName === 'search') {
    renderSearchInterface();
  } else if (tabName === 'calculator') {
    showCalculator();
  } else {
    renderFiles(allFiles, tabName);
  }
}

function showCalculator() {
  document.getElementById('surah-container').style.display = 'none';
  document.getElementById('calculator-container').style.display = 'block';

  // Lazy load calculator script
  if (!calculatorLoaded) {
    const script = document.createElement('script');
    script.src = 'abjad_calculator/apps/quran/template/static/js/abjad-calculator.js';
    script.onload = function() { calculatorLoaded = true; };
    document.head.appendChild(script);
  }
}

function calculateInput() {
  const input = document.getElementById('calculator-input').value;
  const resultsContainer = document.getElementById('calculator-results');

  if (typeof renderCalculatorResult === 'function') {
    renderCalculatorResult(resultsContainer, input);
  }
}
