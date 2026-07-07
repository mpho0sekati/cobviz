from __future__ import annotations

from .parser import CobolModel


def generate_mermaid_flowchart(model: CobolModel) -> str:
    lines = ["flowchart TD"]
    for paragraph in model.paragraphs:
        # Mermaid nodes can have IDs and labels.
        # Using IDs without special characters and labels in quotes or brackets.
        # COBOL paragraph names usually don't have special chars except hyphen.
        lines.append(f'    {paragraph}["{paragraph}"]')

    for source, target in model.edges:
        lines.append(f"    {source} --> {target}")

    return "\n".join(lines)
