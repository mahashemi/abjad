from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

@dataclass
class LetterBreakdown:
    """Represents the numerical breakdown of a single letter."""
    letter: str
    qamari_value: int
    malfuzi_value: int
    bayenati_value: int


@dataclass
class LetterValue:
    """Represents a mapping of a letter to its numerical value."""
    letter: str
    value: int


@dataclass
class VerificationItem:
    """Represents verification data for a single letter."""
    count: int
    qamari_value: int
    total: int


@dataclass
class DivisionResult:
    """Represents the result of division by 3."""
    quotient: int
    remainder: int


@dataclass
class AbjadResult:
    """Represents the complete result of an Abjad calculation."""
    original_text: str
    cleaned_text: str
    total_qamari_value: int = 0
    total_malfuzi_value: int = 0
    total_bayenati_value: int = 0
    breakdown: List[LetterBreakdown] = field(default_factory=list)
    letter_qamari_values: List[LetterValue] = field(default_factory=list)
    letter_malfuzi_values: List[LetterValue] = field(default_factory=list)
    letter_bayenati_values: List[LetterValue] = field(default_factory=list)
    letter_counts: Dict[str, int] = field(default_factory=dict)
    verification: Dict[str, VerificationItem] = field(default_factory=dict)
    verification_total: int = 0


@dataclass
class MusallasProperties:
    """Represents the special properties for musallas calculation."""
    total_minus_12: int
    division_by_3: DivisionResult
    increment_cell: int


class DardLocation(Enum):
    """Enumeration of supported pain locations."""
    SAR = "SAR"       # Head
    KAMAR = "KAMAR"   # Back


@dataclass
class NaqshResult(AbjadResult):
    """Extended AbjadResult with Naqsh-specific properties."""
    naqsh_type: str = ""
    huruf_sawamat: str = ""
    bastam_text: str = ""
    name_with_mothers_name: str = ""
    interleaved_text: str = ""
    hurf_groups: List[List[str]] = field(default_factory=list)
    special_properties: Optional[MusallasProperties] = None
