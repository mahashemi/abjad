# Quran Translation Script

This script translates Quran verses from Arabic/English to Urdu, Persian, and adds transliteration using Claude Sonnet via AWS Bedrock.

## Features

- ✅ Batch processing (10 verses at a time)
- ✅ Progress tracking with automatic resume capability
- ✅ Robust error handling with retry logic
- ✅ Flexible chapter selection via command-line arguments
- ✅ Saves each chapter as a Python file with `ayats` variable
- ✅ Only updates new fields (preserves original data)

## Prerequisites

1. **AWS Credentials**: Configured for Bedrock access
2. **Python 3.8+**
3. **Required packages**: boto3

```bash
pip install boto3
```

## Usage

### Basic Usage

Process all chapters (respects progress file):
```bash
python quran_translator.py
```

### Process Specific Chapters

Process a single chapter:
```bash
python quran_translator.py --chapter 15
```

Process a range of chapters:
```bash
python quran_translator.py --chapters 15-54
```

Process multiple ranges:
```bash
python quran_translator.py --chapters 15-54,60-77
```

### Exclude Chapters

Process chapters 15-77 but exclude 55, 56, 58, 59:
```bash
python quran_translator.py --chapters 15-77 --exclude 55,56,58,59
```

### Your Specific Use Case

Based on your requirements (chapters 1-14 done, need 15-54, skip 55-56,58-59, need 60-77):

```bash
python quran_translator.py --chapters 15-77 --exclude 55,56,58,59
```

Or if you want to process them in separate runs:

```bash
# First batch: chapters 15-54
python quran_translator.py --chapters 15-54

# Second batch: chapters 60-77
python quran_translator.py --chapters 60-77
```

### Advanced Options

Show help:
```bash
python quran_translator.py --help
```

Custom input/output paths:
```bash
python quran_translator.py \
  --input /path/to/quran_bilingual.json \
  --output /path/to/output_dir \
  --progress /path/to/progress.json \
  --chapters 15-77 \
  --exclude 55,56,58,59
```

## Output

Each chapter is saved as a Python file in the `translated_chapters` directory:

```python
"""
Chapter 15: al-hijr
Arabic: الحجر
Total Verses: 99
Generated: 2026-01-12T18:27:00.123456
"""

ayats = [
  {
    "verse_number": 1,
    "arabic_text": "الر ۚ تِلْكَ آيَاتُ الْكِتَابِ وَقُرْآنٍ مُّبِينٍ",
    "english_text": "Alif Laam Ra. These are verses of the Book and a clear Quran.",
    "urdu_text": "الف، لام، را۔ یہ کتاب اور واضح قرآن کی آیات ہیں۔",
    "persian_text": "الف، لام، را. این‌ها آیات کتاب و قرآن روشن است.",
    "transliteration": "Alif-Lam-Ra. Tilka ayatul-Kitabi wa Qur'anin-mubin"
  },
  ...
]
```

## Progress Tracking

The script automatically tracks progress in `translation_progress.json`:

```json
{
  "last_completed_chapter": 15,
  "last_completed_batch_in_chapter": 9,
  "chapters_completed": [15, 16, 17],
  "total_verses_processed": 450,
  "start_time": "2026-01-12T18:00:00",
  "last_update": "2026-01-12T18:30:00"
}
```

### Resume After Interruption

If the script is interrupted (Ctrl+C, error, etc.), simply run it again with the same arguments. It will automatically resume from where it left off.

## Error Handling

- **Automatic Retry**: Bedrock API calls retry up to 3 times with exponential backoff
- **Progress Saving**: Progress is saved after each batch (10 verses)
- **Resume Support**: Can resume from any point after interruption
- **Batch-level Recovery**: If a batch fails, only that batch needs to be retried

## Logs

All operations are logged to:
- Console (INFO level)
- `quran_translation.log` (detailed logging)

## Translation Quality

The script uses Claude Sonnet 3.5 with:
- Temperature: 0.1 (for consistency)
- Max tokens: 16,384
- Structured JSON output with validation

Translations follow these guidelines:
- Simple, clear Urdu translation
- Modern, readable Persian (Farsi)
- Accurate Arabic transliteration (Romanization)
- Respectful and spiritually accurate

## File Structure

```
dad_english_quran_converter/
├── quran_bilingual.json           # Input file
├── quran_translator.py            # Main script
├── translation_progress.json      # Progress tracker
├── quran_translation.log         # Detailed logs
├── README.md                      # This file
└── translated_chapters/           # Output directory
    ├── chapter_001_fatiha.py
    ├── chapter_002_baqra.py
    ├── chapter_015_al-hijr.py
    └── ...
```

## Troubleshooting

### AWS Credentials Not Found
Ensure AWS credentials are configured:
```bash
aws configure
```

### Bedrock Access Denied
Verify your AWS account has Bedrock access and the required model permissions.

### Out of Memory
Reduce batch size by modifying `batch_size` parameter in the `translate_chapter` method.

### JSON Parsing Errors
The script automatically retries failed requests. Check logs for details.

## Cost Estimation

Approximate costs (varies by region):
- Claude Sonnet 3.5: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- Average chapter: ~100-200 verses
- Total Quran: ~6,236 verses

Estimated total cost: $50-$150 depending on verse complexity.

## Support

For issues or questions, check:
1. `quran_translation.log` for detailed error messages
2. `translation_progress.json` for progress status
3. AWS CloudWatch logs for Bedrock API issues
