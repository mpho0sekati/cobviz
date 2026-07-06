from __future__ import annotations

from .parser import CobolModel


def generate_mermaid_flowchart(model: CobolModel) -> str:
    lines = ["flowchart TD"]
    for paragraph in model.paragraphs:
        lines.append(f"    {paragraph}[{paragraph}]")

    for source, target in model.performs:
        lines.append(f"    {source} --> {target}")

    return "\n".join(lines)
