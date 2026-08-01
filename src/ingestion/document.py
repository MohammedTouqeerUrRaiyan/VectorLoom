from dataclasses import dataclass, field 
from typing import Dict, List, Optional, Union

@dataclass
class Document:
      source_path: str
      extracted_text:str
      metadata: Dict[str, Union[str, int, float]] = field(default_factory=dict)
      language: Optional[str] = None
      valid: bool = True
      error: Optional[str] = None

class Document:

    def __init__(
        self,
        source_path,
        extracted_text,
        clean_text,
        metadata,
        language,
        valid,
        error=None,
    ):
        self.source_path = source_path
        self.extracted_text = extracted_text
        self.clean_text = clean_text
        self.metadata = metadata
        self.language = language
        self.valid = valid
        self.error = error

        