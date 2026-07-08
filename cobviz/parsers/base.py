from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, Tuple, Dict

@dataclass(frozen=True)
class ProgramModel:
    paragraphs: Tuple[str, ...]
    edges: Tuple[Tuple[str, str], ...]
    paragraph_comments: Dict[str, str]
    divisions: Tuple[str, ...]
    sections: Dict[str, Tuple[str, ...]]  # Section Name -> List of Paragraphs/Labels
    files: Tuple[str, ...]
    file_usage: Dict[str, Set[str]]  # Paragraph/Label -> Set of Files used
    language: str = "unknown"

class LanguageParser(ABC):
    @abstractmethod
    def parse(self, source: str) -> ProgramModel:
        pass
