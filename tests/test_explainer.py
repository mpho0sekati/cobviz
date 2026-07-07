from cobviz.parser import parse_cobol_source
from cobviz.explainer import explain_cobol_program


def test_explain_cobol_program_basic() -> None:
    source = """
000100 PROCEDURE DIVISION.
* This is the entry point.
000200 START-PARA.
000300     PERFORM PROCESS-PARA.
000400     STOP RUN.
* Processes the data.
000500 PROCESS-PARA.
000600     EXIT.
"""
    model = parse_cobol_source(source)
    explanation = explain_cobol_program(model)

    assert "## COBOL Program Breakdown" in explanation
    assert "Entry Point: `START-PARA`" in explanation
    assert "This is the entry point." in explanation
    assert "Processes the data." in explanation
    assert "`START-PARA` → `PROCESS-PARA`" in explanation


def test_explain_cobol_program_no_paragraphs() -> None:
    source = "000100 IDENTIFICATION DIVISION."
    model = parse_cobol_source(source)
    explanation = explain_cobol_program(model)
    assert "has no identifiable paragraphs" in explanation
