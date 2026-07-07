from __future__ import annotations

from .parser import CobolModel


def explain_cobol_program(model: CobolModel) -> str:
    """Generate a textual breakdown of the COBOL program."""
    if not model.paragraphs:
        return "This COBOL program has no identifiable paragraphs in its PROCEDURE DIVISION."

    lines = ["## COBOL Program Breakdown", ""]

    # Identify entry point (usually first paragraph)
    entry_para = model.paragraphs[0]
    lines.append(f"### Entry Point: `{entry_para}`")
    lines.append(f"The program begins execution at the `{entry_para}` paragraph.")
    lines.append("")

    lines.append("### Paragraphs and Logic")
    for para in model.paragraphs:
        comment = model.paragraph_comments.get(para, "No description available.")
        lines.append(f"#### `{para}`")
        lines.append(f"- **Purpose:** {comment}")

        # Find PERFORMs from this paragraph
        calls = [target for src, target in model.edges if src == para]
        if calls:
            lines.append(f"- **Actions:** Calls the following paragraphs: {', '.join([f'`{c}`' for c in set(calls)])}")
        else:
            lines.append("- **Actions:** This paragraph does not call any others directly.")
        lines.append("")

    lines.append("### Summary of Control Flow")
    if model.edges:
        lines.append("The program uses `PERFORM` statements to create a modular structure. Here is how they connect:")
        for src, target in sorted(set(model.edges)):
            lines.append(f"- `{src}` → `{target}`")
    else:
        lines.append("This is a linear program with no internal `PERFORM` calls.")

    return "\n".join(lines)
