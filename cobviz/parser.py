from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CobolModel:
    paragraphs: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    paragraph_comments: dict[str, str]
    divisions: tuple[str, ...]
    sections: dict[str, tuple[str, ...]]  # Section Name -> List of Paragraphs
    files: tuple[str, ...]


PARAGRAPH_PATTERN = re.compile(r"^(?:[0-9]{6})?\s*([A-Za-z0-9-]+)\.\s*", re.MULTILINE)
SECTION_PATTERN = re.compile(r"^(?:[0-9]{6})?\s*([A-Za-z0-9-]+)\s+SECTION\.\s*$", re.MULTILINE | re.IGNORECASE)
PERFORM_PATTERN = re.compile(r"\bPERFORM\s+([A-Za-z0-9-]+)\b", re.IGNORECASE)
COMMENT_PATTERN = re.compile(r"^(?:[0-9]{6})?\* (.*)$")
SELECT_PATTERN = re.compile(r"\bSELECT\s+([A-Za-z0-9-]+)\b", re.IGNORECASE)

# Security Constants
MAX_PARAGRAPHS = 500
MAX_EDGES = 1000

IGNORED_SUFFIXES = ("-DIVISION", "DIVISION")
IGNORED_PARAGRAPHS = {"EXIT"}


def parse_cobol_source(source: str) -> CobolModel:
    lines = source.splitlines()
    paragraphs: list[str] = []
    edges: list[tuple[str, str]] = []
    paragraph_comments: dict[str, str] = {}
    divisions: list[str] = []
    sections: dict[str, list[str]] = {}
    files: list[str] = []

    current_para: str | None = None
    current_section: str | None = None
    pending_comments: list[str] = []

    for line in lines:
        # Extract SELECT statements for files
        for select_match in SELECT_PATTERN.finditer(line):
            file_name = select_match.group(1).upper()
            if file_name not in files:
                files.append(file_name)

        comment_match = COMMENT_PATTERN.match(line)
        if comment_match:
            pending_comments.append(comment_match.group(1).strip())
            continue

        # Check for division headers
        div_match = re.search(r"([A-Z-]+ DIVISION)", line.upper())
        if div_match:
             divisions.append(div_match.group(1))
             pending_comments = []
             continue

        # Check for section headers
        sect_match = SECTION_PATTERN.match(line)
        if sect_match:
            para_name = sect_match.group(1).upper() + " SECTION"
            current_section = para_name
            if current_section not in sections:
                sections[current_section] = []

            if current_section not in paragraphs:
                if len(paragraphs) >= MAX_PARAGRAPHS:
                    raise ValueError(f"Exceeded maximum number of paragraphs ({MAX_PARAGRAPHS})")
                paragraphs.append(current_section)
            current_para = current_section
            if pending_comments:
                paragraph_comments[current_section] = " ".join(pending_comments)
            pending_comments = []
            continue

        para_match = PARAGRAPH_PATTERN.match(line)
        content_line = line
        if para_match:
            para_name = para_match.group(1).upper()

            if para_name in IGNORED_PARAGRAPHS:
                pending_comments = []
                continue

            if para_name not in paragraphs:
                if len(paragraphs) >= MAX_PARAGRAPHS:
                    raise ValueError(f"Exceeded maximum number of paragraphs ({MAX_PARAGRAPHS})")
                paragraphs.append(para_name)
                if current_section:
                    sections[current_section].append(para_name)

            current_para = para_name
            if pending_comments:
                paragraph_comments[para_name] = " ".join(pending_comments)

            pending_comments = []
            content_line = line[para_match.end():]

        if current_para:
            for perform_match in PERFORM_PATTERN.finditer(content_line):
                if len(edges) >= MAX_EDGES:
                    raise ValueError(f"Exceeded maximum number of edges ({MAX_EDGES})")
                target = perform_match.group(1).upper()
                edges.append((current_para, target))

    return CobolModel(
        paragraphs=tuple(paragraphs),
        edges=tuple(edges),
        paragraph_comments=paragraph_comments,
        divisions=tuple(divisions),
        sections={k: tuple(v) for k, v in sections.items()},
        files=tuple(files)
    )
