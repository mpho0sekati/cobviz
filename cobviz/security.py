from __future__ import annotations

from pathlib import Path

ALLOWED_EXTENSIONS = {".cbl", ".cob", ".cpy"}
NULL_BYTE = b"\x00"


def validate_cobol_path(path: Path) -> Path:
    if not isinstance(path, Path):
        path = Path(path)

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported COBOL extension {path.suffix}. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    # Use Path.resolve() to handle '..' and symlinks
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"COBOL source file not found: {path}")

    if not resolved.is_file():
        raise ValueError(f"Path is not a file: {resolved}")

    # To prevent path traversal, we restrict access to files within the current working directory.
    cwd = Path.cwd().resolve()
    if not str(resolved).startswith(str(cwd)):
        raise ValueError(f"Path traversal detected: {resolved} is outside of the working directory {cwd}")

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
