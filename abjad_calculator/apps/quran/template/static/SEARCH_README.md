# Quran Search Feature

## Overview
Complete multi-language search functionality for the Holy Quran with Abjad numerical values.

## Files Structure

```
template/static/
├── index.html                      # Main page with tabs: Surahs, Duas, Search
├── js/
│   └── search.js                   # Search functionality implementation
├── css/
│   └── style.css                   # Existing styles
├── data/
│   └── quran_search_index.json    # 25MB search index (6,224 verses)
└── SEARCH_README.md                # This file
```

## Features

### Multi-Language Support
- **Arabic** (original text with diacritics)
- **English** (translation)
- **Urdu** (اردو translation)
- **Persian** (فارسی translation)
- **Transliteration** (romanized Arabic)

### Search Capabilities
1. **Text Search**: Search any word or phrase across all languages
2. **Abjad Value Search**: Find verses by numerical values
   - Qamari (القمري)
   - Malfuzi (الملفوظي)
   - Bayenati/Batini (الباطني)
3. **Chapter Filtering**: Search within specific chapters
4. **Language Filtering**: Focus search on specific language(s)

### Data Included Per Verse
- Chapter number and name
- Verse number
- All translations
- Abjad values (verse-level)
- Word count
- Word-level abjad statistics
- Letter counts
- Cleaned text for calculations

## How to Use

### Basic Text Search
1. Click the "البحث" (Search) tab
2. Enter your search term
3. Select language (or leave as "All")
4. Click "بحث Search"

### Abjad Value Search
1. Select abjad system (Qamari/Malfuzi/Bayenati)
2. Enter target value
3. Optionally set tolerance (±)
4. Click "بحث Search"

### Chapter-Specific Search
- Use the chapter dropdown to limit search to specific surah
- Leave as "All" to search entire Quran

## Technical Details

### Data Generation
- Script: `/home/sazmham/personal_apps/abjad/abjad_calculator/common/build_search_index.py`
- Source: `quran_library` + debug folder abjad calculations
- Output: 25MB JSON (compresses to ~5-7MB with gzip on GitHub Pages)

### GitHub Pages Deployment
The static folder is designed to be served directly from GitHub Pages:
- URL will be: `https://mahashemi.github.io/abjad/abjad_calculator/apps/quran/template/static/`
- JSON will auto-compress with gzip
- All resources load from relative paths

## Next Steps (Optional Enhancements)

### Mobile Optimization
- Convert tab navigation to hamburger menu on small screens
- Touch-friendly filters and buttons
- Responsive result cards

### Additional Features
- Search history
- Bookmarks/favorites
- Export search results
- Advanced filters (Meccan/Medinan, Juz, etc.)
- Search result highlighting
- Verse comparison tool
- Statistical dashboard

## Maintenance

### Regenerating Search Index
If verse data or abjad calculations change:
```bash
cd /home/sazmham/personal_apps/abjad/abjad_calculator
PYTHONPATH=/home/sazmham/personal_apps/abjad:$PYTHONPATH python common/build_search_index.py
```

### File Sizes
- `quran_search_index.json`: 25MB uncompressed
- After gzip (GitHub Pages): ~5-7MB
- Load time: 2-5 seconds on decent connection

## Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript ES6+ required
- Fetch API support required

## Credits
- Quran text and translations from quran_library
- Abjad calculations from custom calculator
- UI design matches existing Abjad theme

---
Last Updated: 2026-02-02