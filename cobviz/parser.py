from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CobolModel:
    paragraphs: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]


PARAGRAPH_PATTERN = re.compile(r"^(?:[0-9]{6})?\s*([A-Za-z0-9-]+)\.\s*", re.MULTILINE)
PERFORM_PATTERN = re.compile(r"\bPERFORM\s+([A-Za-z0-9-]+)\b", re.IGNORECASE)

# Security Constants
MAX_PARAGRAPHS = 500
MAX_EDGES = 1000

IGNORED_SUFFIXES = ("-DIVISION", "DIVISION", "-SECTION", "SECTION")
IGNORED_PARAGRAPHS = {"EXIT"}


def parse_cobol_source(source: str) -> CobolModel:
    lines = source.splitlines()
    paragraphs: list[str] = []
    edges: list[tuple[str, str]] = []
    current_para: str | None = None

    for line in lines:
        para_match = PARAGRAPH_PATTERN.match(line)
        content_line = line
        if para_match:
            para_name = para_match.group(1).upper()
            is_ignored = False

            if any(para_name.endswith(suffix) for suffix in IGNORED_SUFFIXES):
                if "SECTION" in para_name:
                    if para_name not in paragraphs:
                        if len(paragraphs) >= MAX_PARAGRAPHS:
                            raise ValueError(f"Exceeded maximum number of paragraphs ({MAX_PARAGRAPHS})")
                        paragraphs.append(para_name)
                    current_para = para_name
                is_ignored = True

            elif para_name in IGNORED_PARAGRAPHS:
                is_ignored = True

            if not is_ignored:
                if para_name not in paragraphs:
                    if len(paragraphs) >= MAX_PARAGRAPHS:
                        raise ValueError(f"Exceeded maximum number of paragraphs ({MAX_PARAGRAPHS})")
                    paragraphs.append(para_name)
                current_para = para_name

            # The rest of the line should be processed for PERFORMs
            content_line = line[para_match.end():]

        if current_para:
            for perform_match in PERFORM_PATTERN.finditer(content_line):
                if len(edges) >= MAX_EDGES:
                    raise ValueError(f"Exceeded maximum number of edges ({MAX_EDGES})")
                target = perform_match.group(1).upper()
                edges.append((current_para, target))

    return CobolModel(paragraphs=tuple(paragraphs), edges=tuple(edges))
