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

def test_parse_cobol_source_extracts_file_usage():
    source = """
000100 ENVIRONMENT DIVISION.
000200 INPUT-OUTPUT SECTION.
000300 FILE-CONTROL.
000400     SELECT MY-FILE ASSIGN TO "DATA.DAT".
000500 PROCEDURE DIVISION.
000600 MAIN-PARA.
000700     OPEN INPUT MY-FILE.
000800     READ MY-FILE.
000900     CLOSE MY-FILE.
001000     STOP RUN.
"""
    model = parse_cobol_source(source)
    assert "MY-FILE" in model.files
    assert "MY-FILE" in model.file_usage["MAIN-PARA"]
