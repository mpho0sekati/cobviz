from __future__ import annotations

from pathlib import Path

ALLOWED_EXTENSIONS = {".cbl", ".cob", ".cpy"}
NULL_BYTE = b"\x00"


def validate_cobol_path(path: Path) -> Path:
    if not isinstance(path, Path):
        path = Path(path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"COBOL source file not found: {path}")

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported COBOL extension {path.suffix}. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    resolved = path.resolve()
    if not str(resolved).startswith(str(path.parent.resolve())):
        raise ValueError("Invalid file path. Path traversal is not allowed.")

    return resolved


def read_cobol_source(path: Path, max_size: int = 10 * 1024 * 1024) -> str:
    size = path.stat().st_size
    if size > max_size:
        raise ValueError(
            f"COBOL source file is too large ({size} bytes). Max size is {max_size} bytes."
        )

    content = path.read_bytes()
    if NULL_BYTE in content:
        raise ValueError("Binary content is not allowed in COBOL source files.")

    text = content.decode("utf-8", errors="strict")
    if text.startswith("\ufeff"):
        text = text[1:]

    return text.replace("\r\n", "\n").replace("\r", "\n")
