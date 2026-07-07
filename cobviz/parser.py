from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CobolModel:
    paragraphs: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    paragraph_comments: dict[str, str]


PARAGRAPH_PATTERN = re.compile(r"^(?:[0-9]{6})?\s*([A-Za-z0-9-]+)\.\s*", re.MULTILINE)
PERFORM_PATTERN = re.compile(r"\bPERFORM\s+([A-Za-z0-9-]+)\b", re.IGNORECASE)
COMMENT_PATTERN = re.compile(r"^(?:[0-9]{6})?\* (.*)$")

# Security Constants
MAX_PARAGRAPHS = 500
MAX_EDGES = 1000

IGNORED_SUFFIXES = ("-DIVISION", "DIVISION", "-SECTION", "SECTION")
IGNORED_PARAGRAPHS = {"EXIT"}


def parse_cobol_source(source: str) -> CobolModel:
    lines = source.splitlines()
    paragraphs: list[str] = []
    edges: list[tuple[str, str]] = []
    paragraph_comments: dict[str, str] = {}
    current_para: str | None = None
    pending_comments: list[str] = []

    for line in lines:
        comment_match = COMMENT_PATTERN.match(line)
        if comment_match:
            pending_comments.append(comment_match.group(1).strip())
            continue

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
                if pending_comments:
                    paragraph_comments[para_name] = " ".join(pending_comments)

            # Reset pending comments after hitting a paragraph
            pending_comments = []
            # The rest of the line should be processed for PERFORMs
            content_line = line[para_match.end():]
        elif line.strip() and not comment_match:
             # If it is not a comment and not a paragraph header,
             # it is probably code, so reset pending comments?
             # Actually, comments can be between lines of code.
             # But for simplicity, we only associate comments immediately preceding a paragraph.
             # However, if we hit code, we should probably clear pending_comments if they were intended for code.
             pass

        if current_para:
            for perform_match in PERFORM_PATTERN.finditer(content_line):
                if len(edges) >= MAX_EDGES:
                    raise ValueError(f"Exceeded maximum number of edges ({MAX_EDGES})")
                target = perform_match.group(1).upper()
                edges.append((current_para, target))

    return CobolModel(
        paragraphs=tuple(paragraphs),
        edges=tuple(edges),
        paragraph_comments=paragraph_comments
    )
