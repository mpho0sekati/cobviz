from __future__ import annotations
from pathlib import Path
from .parsers.base import ProgramModel, LanguageParser
from .parsers.cobol import CobolParser
from .parsers.pli import PLIParser
from .parsers.rpg import RPGParser
from .parsers.natural import NaturalParser
from .parsers.assembler import AssemblerParser

def get_parser_for_file(filename: str) -> LanguageParser:
    ext = Path(filename).suffix.lower()
    if ext in ('.cob', '.cbl', '.cobol', '.cpy'):
        return CobolParser()
    elif ext in ('.pli', '.pl1'):
        return PLIParser()
    elif ext in ('.rpg', '.rpgle'):
        return RPGParser()
    elif ext in ('.nsn', '.nsp', '.nsh'):
        return NaturalParser()
    elif ext in ('.asm', '.s'):
        return AssemblerParser()
    return CobolParser() # Default to COBOL

def parse_source(source: str, filename: str = "program.cob") -> ProgramModel:
    parser = get_parser_for_file(filename)
    return parser.parse(source)

# Maintain compatibility with existing code that might still call parse_cobol_source
def parse_cobol_source(source: str) -> ProgramModel:
    return CobolParser().parse(source)
