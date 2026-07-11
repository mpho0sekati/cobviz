from .base import LanguageParser, ProgramModel

class PLIParser(LanguageParser):
    def parse(self, source: str) -> ProgramModel:
        # Stub for PL/I parsing
        return ProgramModel(tuple(), tuple(), {}, tuple(), {}, tuple(), {}, "PL/I")
