from __future__ import annotations
import requests
from typing import List, Dict, Optional
from .base import IntelligenceProvider
from .factory import ProviderRegistry

class OllamaProvider(IntelligenceProvider):
    """
    Provider for local Ollama instances.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3", **kwargs):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def _request(self, prompt: str, system: Optional[str] = None) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data['response']
        except Exception as e:
            return f"Error from Ollama: {str(e)}"

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Ollama has a chat API but we can simulate with generate for simplicity
        return self._request(messages[-1]['content'])

    def summarize(self, text: str) -> str:
        return self._request(f"Summarize this code:\n\n{text}")

    def explain(self, code: str, context: Optional[str] = None) -> str:
        prompt = f"Explain this code logic:\n\n{code}"
        if context:
            prompt += f"\n\nContext: {context}"
        return self._request(prompt)

    def generateDocumentation(self, code: str) -> str:
        return self._request(f"Generate technical documentation for this code:\n\n{code}")

    def analyzeBusinessRules(self, code: str) -> str:
        return self._request(f"Extract business rules from this code:\n\n{code}")

    def impactAnalysis(self, code: str, change_description: str) -> str:
        return self._request(f"Analyze the impact of this change: {change_description}\n\nOn this code:\n\n{code}")

    def securityReview(self, code: str) -> str:
        return self._request(f"Perform a security review of this code:\n\n{code}")

# Register the provider
ProviderRegistry.register("ollama", OllamaProvider)
