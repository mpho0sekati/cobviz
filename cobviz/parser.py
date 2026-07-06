from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CobolModel:
    paragraphs: tuple[str, ...]
    performs: tuple[tuple[str, str], ...]


PARAGRAPH_PATTERN = re.compile(r"^([A-Za-z0-9-]+)\.?\s*$", re.MULTILINE)
PERFORM_PATTERN = re.compile(r"\bPERFORM\s+([A-Za-z0-9-]+)\b", re.IGNORECASE)


def parse_cobol_source(source: str) -> CobolModel:
    paragraphs = tuple({match.group(1).upper() for match in PARAGRAPH_PATTERN.finditer(source)})
    performs = tuple(
        (match.group(0).upper(), match.group(1).upper())
        for match in PERFORM_PATTERN.finditer(source)
    )
    return CobolModel(paragraphs=paragraphs, performs=performs)
