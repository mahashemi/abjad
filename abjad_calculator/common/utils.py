"""
utils.py Utility functions for the Abjad Calculator.
"""
from pathlib import Path
import logging

from .constants import REMOVE_CHARS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def clean_text(text):
    """Clean Arabic text by removing diacritics and standardizing characters."""
    # Replace alif wasla with regular alif
    text = text.replace('ٱ', 'ا')
    
    # Remove diacritics and whitespace
    for char in REMOVE_CHARS:
        text = text.replace(char, '')
    
    return text

def normalize_space_separated_text(text):
    """Convert space-separated characters to a clean list without empty entries."""
    return [c.strip() for c in text.split() if c.strip()]

def interleave_texts(text1, text2):
    """Interleave two character lists."""
    chars1 = text1 if isinstance(text1, list) else normalize_space_separated_text(text1)
    chars2 = text2 if isinstance(text2, list) else normalize_space_separated_text(text2)
    
    interleaved = []
    for i in range(max(len(chars1), len(chars2))):
        if i < len(chars1):
            interleaved.append(chars1[i])
        if i < len(chars2):
            interleaved.append(chars2[i])
    
    return interleaved

def split_into_groups(text_list, group_size=4):
    """Split a list of characters into groups of specified size."""
    groups = []
    for i in range(0, len(text_list), group_size):
        group = text_list[i:i + group_size]
        groups.append(''.join(group))
    return groups

def format_custom_output(result):
    """Format the calculation result into the custom output format."""
    return str(result['letter_values'][::-1])

def create_output_dir(output_dir):
    output_path = Path(output_dir) 
    if not output_path.exists():
        logger.info(f"Creating output directory: {output_path}")
        output_path.mkdir(parents=True)
