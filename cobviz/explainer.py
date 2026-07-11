from __future__ import annotations
from .parsers.base import ProgramModel
from .intelligence import IntelligenceProvider


def explain_program(model: ProgramModel, provider: IntelligenceProvider | None = None) -> str:
    """Generate a textual breakdown of the program."""
    if not model.paragraphs:
        return f"This {model.language} program has no identifiable paragraphs or labels."

    lines = [f"## {model.language} Program Breakdown", ""]

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

        # Files used by this paragraph
        files = model.file_usage.get(para, [])
        if files:
            lines.append(f"- **File Access:** Interacts with {', '.join([f'`{f}`' for f in files])}")

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

    if provider:
        lines.append("")
        lines.append("### AI-Powered Insight")
        # Combine comments as context
        context = " ".join(model.paragraph_comments.values())
        ai_explanation = provider.explain(f"Language: {model.language}\nControl Flow: {model.edges}", context=context)
        lines.append(ai_explanation)

    return "\n".join(lines)


def explain_architecture(model: ProgramModel, provider: IntelligenceProvider | None = None) -> str:
    """Generate a high-level architectural overview."""
    lines = ["## Architectural Overview", ""]

    if model.file_usage:
        lines.append("### Key Data Flows")
        for para, files in model.file_usage.items():
            lines.append(f"- Paragraph `{para}` accesses: {', '.join([f'`{f}`' for f in files])}")
        lines.append("")

    lines.append("### Program Structure")
    if model.divisions:
        lines.append(f"The program consists of the following divisions: {', '.join([f'`{d}`' for d in model.divisions])}.")

    if model.sections:
        lines.append(f"It is organized into {len(model.sections)} logical sections:")
        for section, paras in model.sections.items():
            lines.append(f"- **`{section}`**: Contains {len(paras)} paragraphs ({', '.join([f'`{p}`' for p in paras])}).")
    else:
        lines.append("The program has a flat structure with no explicit sections.")

    lines.append("")
    lines.append("### External Interfaces")
    if model.files:
        lines.append("The program interacts with the following external files:")
        for file in model.files:
            lines.append(f"- **`{file}`**")
    else:
        lines.append("No external file interfaces (SELECT statements) were identified.")

    if provider:
        lines.append("")
        lines.append("### AI Architecture Analysis")
        lines.append(provider.summarize(f"Divisions: {model.divisions}\nFiles: {model.files}"))

    return "\n".join(lines)

def analyze_business_rules(model: ProgramModel, provider: IntelligenceProvider) -> str:
    """Use AI to extract business rules from the program model."""
    context = f"Language: {model.language}\nStructure: {model.sections}"
    return provider.analyzeBusinessRules(context)

def security_review(model: ProgramModel, provider: IntelligenceProvider) -> str:
    """Use AI to perform a security review."""
    return provider.securityReview(f"Language: {model.language}\nFiles: {model.files}")
