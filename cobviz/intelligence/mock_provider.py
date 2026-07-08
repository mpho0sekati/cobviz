from __future__ import annotations
from typing import List, Dict, Optional
from .base import IntelligenceProvider
from .factory import ProviderRegistry

class MockProvider(IntelligenceProvider):
    """A mock provider for testing and fallback without AI."""

    def __init__(self, **kwargs):
        pass

    def chat(self, messages: List[Dict[str, str]]) -> str:
        return "This is a mock response. Configure a real Intelligence Provider for AI capabilities."

    def summarize(self, text: str) -> str:
        return f"Summary: {text[:100]}..."

    def explain(self, code: str, context: Optional[str] = None) -> str:
        return f"Explanation for code: {code[:100]}..."

    def generateDocumentation(self, code: str) -> str:
        return f"Technical Documentation for code: {code[:100]}..."

    def analyzeBusinessRules(self, code: str) -> str:
        return "Business Rules: 1. Logic flows from top to bottom."

    def impactAnalysis(self, code: str, change_description: str) -> str:
        return f"Impact of '{change_description}': Minimal."

    def securityReview(self, code: str) -> str:
        return "Security Review: No critical vulnerabilities found in mock analysis."

# Register the mock provider
ProviderRegistry.register("mock", MockProvider)
