from __future__ import annotations

from .parsers.base import ProgramModel
from .sanitize import sanitize_mermaid_label, sanitize_node_id


def generate_mermaid_flowchart(model: ProgramModel) -> str:
    lines = ["flowchart TD"]

    # Map original names to sanitized node IDs
    node_map = {name: sanitize_node_id(name) for name in model.paragraphs}

    for original_name, node_id in node_map.items():
        label = sanitize_mermaid_label(original_name)
        lines.append(f'    {node_id}["{label}"]')

    for source, target in model.edges:
        src_id = node_map.get(source, sanitize_node_id(source))
        tgt_id = node_map.get(target, sanitize_node_id(target))
        lines.append(f"    {src_id} --> {tgt_id}")

    return "\n".join(lines)


def generate_architecture_diagram(model: ProgramModel) -> str:
    """Generate a high-level architecture diagram showing Sections and Files."""
    lines = ["flowchart LR"]

    # Files as database nodes
    for file_name in model.files:
        safe_file = sanitize_node_id(file_name)
        lines.append(f'    {safe_file}[("{file_name}")]')

    # Sections as subgraphs
    for section_name, paragraphs in model.sections.items():
        safe_section = sanitize_node_id(section_name)
        lines.append(f"    subgraph {safe_section} [{section_name}]")
        for para in paragraphs:
            safe_para = sanitize_node_id(para)
            label = sanitize_mermaid_label(para)
            lines.append(f'        {safe_para}["{label}"]')
        lines.append("    end")

    # If there are no sections, just show paragraphs
    if not model.sections:
        for para in model.paragraphs:
            safe_para = sanitize_node_id(para)
            label = sanitize_mermaid_label(para)
            lines.append(f'    {safe_para}["{label}"]')

    # Edges between sections/paragraphs (summarized or full)
    for source, target in set(model.edges):
        src_id = sanitize_node_id(source)
        tgt_id = sanitize_node_id(target)
        lines.append(f"    {src_id} --> {tgt_id}")

    # Edges between paragraphs and files they use
    for para, files in model.file_usage.items():
        para_id = sanitize_node_id(para)
        for file_name in files:
            file_id = sanitize_node_id(file_name)
            lines.append(f"    {para_id} -.-> {file_id}")

    return "\n".join(lines)
