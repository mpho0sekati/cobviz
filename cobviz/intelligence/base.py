from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IntelligenceProvider(ABC):
    """
    Abstract base class for all AI/Intelligence providers in CobViz.
    Decouples the application from specific AI vendors or local models.
    """

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Generic chat interface."""
        pass

    @abstractmethod
    def summarize(self, text: str) -> str:
        """Summarize the provided source code or documentation."""
        pass

    @abstractmethod
    def explain(self, code: str, context: Optional[str] = None) -> str:
        """Explain the logic of the provided code block."""
        pass

    @abstractmethod
    def generateDocumentation(self, code: str) -> str:
        """Generate technical documentation for the code."""
        pass

    @abstractmethod
    def analyzeBusinessRules(self, code: str) -> str:
        """Extract and explain business rules from the code."""
        pass

    @abstractmethod
    def impactAnalysis(self, code: str, change_description: str) -> str:
        """Analyze the impact of a proposed change."""
        pass

    @abstractmethod
    def securityReview(self, code: str) -> str:
        """Perform a security review of the code (e.g., finding vulnerabilities)."""
        pass
