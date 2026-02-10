from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ResumeData:
    raw_text: str
    lines: List[str]
    word_count: int
    header_text: str
    footer_text: str
    bullets: List[str]
    sections: Dict[str, List[str]]  
