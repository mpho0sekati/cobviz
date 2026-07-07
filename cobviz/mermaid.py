from __future__ import annotations

from .parser import CobolModel
from .sanitize import sanitize_mermaid_label, sanitize_node_id


def generate_mermaid_flowchart(model: CobolModel) -> str:
    lines = ["flowchart TD"]

    # Map original names to sanitized node IDs
    node_map = {name: sanitize_node_id(name) for name in model.paragraphs}

    for original_name, node_id in node_map.items():
        label = sanitize_mermaid_label(original_name)
        lines.append(f'    {node_id}["{label}"]')

    for source, target in model.edges:
        # We need to sanitize source and target in case they are not in paragraphs
        # (e.g. if a PERFORM target is not defined as a paragraph)
        src_id = node_map.get(source, sanitize_node_id(source))
        tgt_id = node_map.get(target, sanitize_node_id(target))
        lines.append(f"    {src_id} --> {tgt_id}")

    return "\n".join(lines)
