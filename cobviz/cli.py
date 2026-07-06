from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .mermaid import generate_mermaid_flowchart
from .parser import parse_cobol_source
from .security import read_cobol_source, validate_cobol_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid flowchart from COBOL source code."
    )
    parser.add_argument("source", type=Path, help="COBOL source file path")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional Mermaid output file path",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=10 * 1024 * 1024,
        help="Maximum COBOL source file size in bytes",
    )

    args = parser.parse_args(argv)
    source_path = validate_cobol_path(args.source)
    source_text = read_cobol_source(source_path, max_size=args.max_size)
    model = parse_cobol_source(source_text)
    diagram = generate_mermaid_flowchart(model)

    if args.output:
        args.output.write_text(diagram, encoding="utf-8")
        return 0

    print(diagram)
    return 0
