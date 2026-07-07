from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .mermaid import generate_mermaid_flowchart
from .parser import parse_cobol_source
from .security import read_cobol_source, validate_cobol_path
from .web import run_web


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid flowchart from COBOL source code."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate diagram from file")
    gen_parser.add_argument("source", type=Path, help="COBOL source file path")
    gen_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional Mermaid output file path",
    )
    gen_parser.add_argument(
        "--max-size",
        type=int,
        default=10 * 1024 * 1024,
        help="Maximum COBOL source file size in bytes",
    )

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Launch web interface")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host address")
    serve_parser.add_argument("--port", type=int, default=5000, help="Port number")
    serve_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args(argv)

    if args.command == "serve":
        run_web(host=args.host, port=args.port, debug=args.debug)
        return 0

    if args.command == "generate" or (not args.command and hasattr(args, "source")):
        # Compatibility with old single-command CLI if possible
        source = getattr(args, "source", None)
        if not source:
             parser.print_help()
             return 1

        source_path = validate_cobol_path(source)
        source_text = read_cobol_source(source_path, max_size=args.max_size)
        model = parse_cobol_source(source_text)
        diagram = generate_mermaid_flowchart(model)

        if args.output:
            args.output.write_text(diagram, encoding="utf-8")
            return 0

        print(diagram)
        return 0

    parser.print_help()
    return 1
