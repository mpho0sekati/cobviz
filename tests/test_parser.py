from cobviz.parser import parse_cobol_source


def test_parse_cobol_source_extracts_paragraphs_and_performs() -> None:
    source = """
000100 IDENTIFICATION DIVISION.
000200 PROCEDURE DIVISION.
000300 MAIN-PARA.
000400     PERFORM PROCESS-DATA
000500     STOP RUN.
000600 PROCESS-DATA.
000700     PERFORM SUB-PARA
000800     EXIT.
000900 SUB-PARA.
001000     EXIT.
"""
    model = parse_cobol_source(source)

    assert "MAIN-PARA" in model.paragraphs
    assert "PROCESS-DATA" in model.paragraphs
    assert "SUB-PARA" in model.paragraphs
    assert "IDENTIFICATION DIVISION" not in model.paragraphs

    assert ("MAIN-PARA", "PROCESS-DATA") in model.edges
    assert ("PROCESS-DATA", "SUB-PARA") in model.edges
