from pathlib import Path

from cobviz.security import read_cobol_source, validate_cobol_path


def test_validate_cobol_path_accepts_allowed_extension(tmp_path: Path) -> None:
    path = tmp_path / "sample.cbl"
    path.write_text("IDENTIFICATION DIVISION.")

    assert validate_cobol_path(path) == path.resolve()


def test_read_cobol_source_rejects_null_bytes(tmp_path: Path) -> None:
    path = tmp_path / "sample.cbl"
    path.write_bytes(b"IDENTIFICATION\x00DIVISION.")

    try:
        read_cobol_source(path)
        assert False, "Expected ValueError for binary content"
    except ValueError as error:
        assert "Binary content is not allowed" in str(error)
