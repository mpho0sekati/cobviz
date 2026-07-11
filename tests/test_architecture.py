from cobviz.parser import parse_cobol_source
from cobviz.mermaid import generate_architecture_diagram
from cobviz.explainer import explain_architecture


def test_architectural_extraction() -> None:
    source = """
000100 IDENTIFICATION DIVISION.
000150 ENVIRONMENT DIVISION.
000160 INPUT-OUTPUT SECTION.
000170 FILE-CONTROL.
000180     SELECT DATA-FILE ASSIGN TO "DATA.DAT".
000200 PROCEDURE DIVISION.
000210 INIT-SECTION SECTION.
000220 START-PARA.
000230     PERFORM PROCESS-PARA.
000240 PROCESS-PARA.
000250     EXIT.
"""
    model = parse_cobol_source(source)

    assert "IDENTIFICATION DIVISION" in model.divisions
    assert "ENVIRONMENT DIVISION" in model.divisions
    assert "DATA-FILE" in model.files
    assert "INIT-SECTION SECTION" in model.sections
    assert "START-PARA" in model.sections["INIT-SECTION SECTION"]
    assert "PROCESS-PARA" in model.sections["INIT-SECTION SECTION"]


def test_generate_architecture_diagram() -> None:
    source = """
000100 ENVIRONMENT DIVISION.
000180     SELECT MY-FILE ASSIGN TO "DATA.DAT".
000200 PROCEDURE DIVISION.
000210 MY-SECTION SECTION.
000220 MY-PARA.
000230     EXIT.
"""
    model = parse_cobol_source(source)
    diagram = generate_architecture_diagram(model)

    assert 'MY_FILE[("MY-FILE")]' in diagram
    assert "subgraph MY_SECTION_SECTION [MY-SECTION SECTION]" in diagram
    assert 'MY_PARA["MY-PARA"]' in diagram


def test_explain_architecture() -> None:
    source = """
000100 ENVIRONMENT DIVISION.
000180     SELECT FILE-A ASSIGN TO "A.DAT".
000200 PROCEDURE DIVISION.
000210 S1 SECTION.
000220 P1. EXIT.
"""
    model = parse_cobol_source(source)
    explanation = explain_architecture(model)

    assert "## Architectural Overview" in explanation
    assert "ENVIRONMENT DIVISION" in explanation
    assert "FILE-A" in explanation
    assert "S1 SECTION" in explanation
