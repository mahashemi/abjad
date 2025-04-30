"""
Arabic Abjad Calculator Package
A modular toolkit for Abjad numerical calculation in Arabic text.
"""

# Import main functions for easy access
from .common.core import calculate_abjad, calculate_musallas_properties
from .common.display import calculate_arabic_text_with_table, calculate_multiple_texts_with_tables
from .apps.naqsh_sawamat.naqsh_calculator import generate_naqsh_musallas
from .apps.quran.quran_calculator import calculate_quranic_verse, process_multiple_verses
from .common.utils import format_custom_output, create_output_dir
from .apps.naqsh_sawamat.naqsh_calculator import generate_sawamat_naqsh_html
from .common.surah_factory import quran

# Version
__version__ = '1.0.0'
