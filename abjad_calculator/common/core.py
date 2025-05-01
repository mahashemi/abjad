"""
core.py: Core functions for Abjad numerical calculation.

This module provides functionality to calculate the Abjad numerical values
of Arabic text using both Qamari and Malfuzi systems.
"""


from .model import AbjadResult, MusallasProperties, LetterBreakdown, LetterValue, VerificationItem, DivisionResult
from .utils import clean_text
from .constants import QAMARI_VALUES, MALFUZI_QAMARI_VALUES, BAYENATI_VALUES


def calculate_abjad(text: str) -> AbjadResult:
    """
    Calculate the Abjad numerical value of Arabic text.
    
    Args:
        text: The Arabic text to calculate Abjad values for
        
    Returns:
        A comprehensive AbjadResult object containing all calculation details
    """
    original_text = text
    cleaned_text = clean_text(text)
    
    # Initialize result
    result = AbjadResult(
        original_text=original_text,
        cleaned_text=cleaned_text
    )
    
    # Calculate letter by letter
    for char in cleaned_text:
        if char.strip():
            qamari_value = 0
            malfuzi_value = 0
            bayenati_value = 0
            if char in QAMARI_VALUES.keys():
                qamari_value = QAMARI_VALUES[char]
                malfuzi_value = MALFUZI_QAMARI_VALUES[char]
                bayenati_value = BAYENATI_VALUES[char]
                
            # Update result with letter information
            result.breakdown.append(LetterBreakdown(
                letter=char,
                qamari_value=qamari_value,
                malfuzi_value=malfuzi_value,
                bayenati_value=bayenati_value
            ))
            result.letter_qamari_values.append(LetterValue(letter=char, value=qamari_value))
            result.letter_malfuzi_values.append(LetterValue(letter=char, value=malfuzi_value))
            result.letter_bayenati_values.append(LetterValue(letter=char, value=bayenati_value))
            result.total_qamari_value += qamari_value
            result.total_malfuzi_value += malfuzi_value
            result.total_bayenati_value += bayenati_value
            
            # Count occurrences of each letter
            result.letter_counts[char] = result.letter_counts.get(char, 0) + 1
    
    # Add verification data
    verification_total = 0
    
    for letter, count in result.letter_counts.items():
        if letter in QAMARI_VALUES.keys():
            value = QAMARI_VALUES[letter]
        else:
            value = 0
        sub_total = count * value
        verification_total += sub_total
        result.verification[letter] = VerificationItem(
            count=count,
            qamari_value=value,
            total=sub_total
        )
    
    result.verification_total = verification_total
    
    return result


def calculate_musallas_properties(abjad_result: AbjadResult) -> MusallasProperties:
    """
    Calculate special properties for musallas from the abjad total.
    
    Args:
        abjad_result: The result from calculate_abjad function
        
    Returns:
        A MusallasProperties object containing derived calculations
    """
    total = abjad_result.total_qamari_value
    total_minus_12 = total - 12
    
    quotient, remainder = divmod(total_minus_12, 3)
    increment_cell = 2 if remainder == 2 else 7
    
    return MusallasProperties(
        total_minus_12=total_minus_12,
        division_by_3=DivisionResult(
            quotient=quotient,
            remainder=remainder
        ),
        increment_cell=increment_cell
    )