import re
from typing import List

class DataRedactor:
    # Common sensitive patterns
    PATTERNS = {
        "email": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        "ipv4": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
        "api_key": re.compile(r'(?:key|token|secret|password|auth)["\s:]+[A-Za-z0-9-]{16,}', re.IGNORECASE)
    }

    def redact(self, text: str) -> str:
        redacted = text
        for label, pattern in self.PATTERNS.items():
            redacted = pattern.sub(f"[REDACTED_{label.upper()}]", redacted)
        return redacted

    def detect_sensitive(self, text: str) -> List[str]:
        found = []
        for label, pattern in self.PATTERNS.items():
            if pattern.search(text):
                found.append(label)
        return found

# Global instance
redactor = DataRedactor()
