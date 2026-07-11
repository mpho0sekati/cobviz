from __future__ import annotations

import re

# Characters that need escaping in Mermaid labels
MERMAID_LABEL_ESCAPE = {
    '[': '(',
    ']': ')',
    '(': '(',
    ')': ')',
    '{': '(',
    '}': ')',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
}


def sanitize_mermaid_label(text: str) -> str:
    """Sanitize and escape special Mermaid characters in labels."""
    for char, replacement in MERMAID_LABEL_ESCAPE.items():
        text = text.replace(char, replacement)

    # Limit length to prevent extreme diagram sizes
    if len(text) > 100:
        text = text[:97] + "..."

    return text


def sanitize_node_id(name: str) -> str:
    """Ensure node IDs contain only safe characters for Mermaid."""
    # Only allow alphanumeric and underscores for node IDs
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    return sanitized[:50]
