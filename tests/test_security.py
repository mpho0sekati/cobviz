import pytest
from pathlib import Path
from cobviz.security import read_cobol_source, validate_cobol_path
from cobviz.parser import parse_cobol_source, MAX_PARAGRAPHS
from cobviz.sanitize import sanitize_mermaid_label, sanitize_node_id
from cobviz.mermaid import generate_mermaid_flowchart, CobolModel


def test_validate_cobol_path_accepts_allowed_extension(tmp_path: Path) -> None:
    # We must ensure the file is within the CWD for the traversal check to pass
    cwd = Path.cwd().resolve()
    path = cwd / "sample.cbl"
    path.write_text("IDENTIFICATION DIVISION.")
    try:
        assert validate_cobol_path(path) == path.resolve()
    finally:
        if path.exists():
            path.unlink()


def test_validate_cobol_path_rejects_traversal(tmp_path: Path) -> None:
    # Create a file outside CWD.
    # Since we can't easily go "outside" the sandbox, let's create a subdirectory and pretend it's CWD.
    cwd = Path.cwd().resolve()
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()

    outside_file = tmp_path / "outside.cbl"
    outside_file.write_text("...")

    import os
    old_cwd = os.getcwd()
    os.chdir(sandbox)
    try:
        with pytest.raises(ValueError, match="Path traversal detected"):
             validate_cobol_path(outside_file)
    finally:
        os.chdir(old_cwd)


def test_read_cobol_source_rejects_null_bytes(tmp_path: Path) -> None:
    path = tmp_path / "sample.cbl"
    path.write_bytes(b"IDENTIFICATION\x00DIVISION.")
    with pytest.raises(ValueError, match="Binary content is not allowed"):
        read_cobol_source(path)


def test_sanitize_mermaid_label() -> None:
    assert sanitize_mermaid_label('PARA "NAME" <TAG>') == 'PARA &quot;NAME&quot; &lt;TAG&gt;'
    sanitized_long = sanitize_mermaid_label('[' + 'A' * 200 + ']')
    assert len(sanitized_long) == 100
    assert sanitized_long.endswith("...")


def test_sanitize_node_id() -> None:
    assert sanitize_node_id("MY-PARA-1") == "MY_PARA_1"
    assert sanitize_node_id("PARA!@#") == "PARA___"


def test_complexity_limit_paragraphs() -> None:
    source = "\n".join([f"PARA-{i}.\n    EXIT." for i in range(MAX_PARAGRAPHS + 1)])
    with pytest.raises(ValueError, match="Exceeded maximum number of paragraphs"):
        parse_cobol_source(source)


def test_mermaid_injection_prevention() -> None:
    model = CobolModel(
        paragraphs=('PARA"; ERROR',),
        edges=(('PARA"; ERROR', 'TARGET'),)
    )
    diagram = generate_mermaid_flowchart(model)
    assert 'PARA___ERROR["PARA&quot;; ERROR"]' in diagram
    assert 'PARA___ERROR --> TARGET' in diagram

def test_parser_processes_remainder_of_line() -> None:
    source = "000100 MAIN-PARA. PERFORM SUB-PARA.\n000200 SUB-PARA.\n000300     EXIT."
    model = parse_cobol_source(source)
    assert "MAIN-PARA" in model.paragraphs
    assert ("MAIN-PARA", "SUB-PARA") in model.edges
