from dataclasses import dataclass, field
from typing import Dict, Optional, Union


@dataclass
class Document:

    source_path: str

    extracted_text: str

    clean_text: str = ""

    pages: int = 0

    metadata: Dict[str, Union[str, int, float]] = field(
        default_factory=dict
    )

    language: Optional[str] = None

    valid: bool = True

    error: Optional[str] = None