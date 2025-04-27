"""
naqsh.py Functions for Naqsh generation and calculation.
"""

from typing import Union
from ...common.model import DardLocation, NaqshResult
from ...common.display import render_naqsh_html
from ...common.constants import PRESET_TEXTS
from ...common.core import calculate_abjad, calculate_musallas_properties
from ...common.utils import normalize_space_separated_text, interleave_texts, split_into_groups

def generate_naqsh_musallas(
    name_with_mothers_name: str, 
    dard_location: Union[str, DardLocation], 
    is_sawamat: bool = False
) -> NaqshResult:
    """
    Generate a Naqsh for pain relief using name and huruf sawamat.
    
    Args:
        name_with_mothers_name: Name and mother's name in space-separated Arabic letters
        dard_location: Location of pain - either "SAR" (head) or "KAMAR" (back)
        is_sawamat: Whether to use huruf sawamat in the calculation
        
    Returns:
        Complete naqsh calculation results as a NaqshResult object
        
    Raises:
        ValueError: If an unsupported dard_location is provided
    """
    # Use default or custom huruf sawamat
    # Handle string or enum input for dard_location
    if isinstance(dard_location, str):
        try:
            dard_location = DardLocation(dard_location)
        except ValueError:
            raise ValueError(f'Unsupported Dard Location: {dard_location}. '
                            f'Supported locations: {", ".join([loc.value for loc in DardLocation])}')
    
    # Use default huruf sawamat if needed
    huruf_sawamat = PRESET_TEXTS["huruf_sawamat"] if is_sawamat else ""
    
    # Select bastam text based on pain location
    if dard_location == DardLocation.SAR:
        bastam_text = PRESET_TEXTS["bastam_dard_sar"]
    elif dard_location == DardLocation.KAMAR:
        bastam_text = PRESET_TEXTS["bastam_dard_kamar"]
    else:
        raise ValueError(f'Unsupported Dard Location: {dard_location}')


    # Process the texts
    name_chars = normalize_space_separated_text(name_with_mothers_name)
    sawamat_chars = normalize_space_separated_text(huruf_sawamat)
    bastam_chars = normalize_space_separated_text(bastam_text)
    
    # Combine bastam with name
    combined_text = bastam_chars + name_chars
    
    # Interleave huruf sawamat with combined text
    interleaved_chars = interleave_texts(sawamat_chars, combined_text)
    interleaved_text = ' '.join(interleaved_chars)
    
    # Calculate abjad value
    abjad_result = calculate_abjad(interleaved_text)
    
    # Create NaqshResult from AbjadResult
    musallas_result = NaqshResult(
        original_text=abjad_result.original_text,
        cleaned_text=abjad_result.cleaned_text,
        total_qamari_value=abjad_result.total_qamari_value,
        total_malfuzi_value=abjad_result.total_malfuzi_value,
        breakdown=abjad_result.breakdown,
        letter_qamari_values=abjad_result.letter_qamari_values,
        letter_malfuzi_values=abjad_result.letter_malfuzi_values,
        letter_counts=abjad_result.letter_counts,
        verification=abjad_result.verification,
        verification_total=abjad_result.verification_total,
        # Naqsh-specific fields
        naqsh_type=f'dard_{dard_location.value.lower()}',
        huruf_sawamat=huruf_sawamat,
        bastam_text=bastam_text,
        name_with_mothers_name=name_with_mothers_name,
        interleaved_text=interleaved_text
    )
    
    # Create groups of 4 for the naqsh squares
    grouped_chars = split_into_groups(interleaved_chars)

    musallas_result.hurf_groups = grouped_chars
    
    return musallas_result

def generate_sawamat_naqsh_html(
    name_with_mothers_name: str,
    dard_location: Union[str, DardLocation] = None, 
    output_html: bool = False, 
    output_path: str = None, 
    show_summary: bool = False, 
    chars_per_row: int = 18
) -> str:
    """
    Generate a Naqsh using huruf sawamat and output detailed HTML report.
    
    Args:
        name_with_mothers_name: Name and mother's name in space-separated Arabic letters
        dard_location: Location of pain, either DardLocation.SAR or DardLocation.KAMAR
        custom_sawamat: Custom huruf sawamat. If None, defaults to preset
        output_html: Whether to save HTML output to a file
        output_path: Path to save HTML output
        show_summary: Whether to show detailed letter summary table
        chars_per_row: Maximum number of characters per row in letter tables
        
    Returns:
        HTML string output
    """

    naqsh_result: NaqshResult = generate_naqsh_musallas(
        name_with_mothers_name=name_with_mothers_name,
        dard_location=dard_location,
        is_sawamat=True
    )
    
    # Calculate musallas properties
    special_props = calculate_musallas_properties(naqsh_result)
    naqsh_result.special_properties = special_props
    
    # Generate HTML
    html_output = render_naqsh_html(
        naqsh_result, 
        output_html, 
        output_path,
        show_summary,
        chars_per_row
    )
    
    return html_output
