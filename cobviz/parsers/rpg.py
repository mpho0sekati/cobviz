from .base import LanguageParser, ProgramModel

class RPGParser(LanguageParser):
    def parse(self, source: str) -> ProgramModel:
        # Stub for RPG parsing
        return ProgramModel(tuple(), tuple(), {}, tuple(), {}, tuple(), {}, "RPG")
