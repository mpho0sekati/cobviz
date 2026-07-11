from .base import LanguageParser, ProgramModel

class NaturalParser(LanguageParser):
    def parse(self, source: str) -> ProgramModel:
        # Stub for Natural parsing
        return ProgramModel(tuple(), tuple(), {}, tuple(), {}, tuple(), {}, "Natural")
