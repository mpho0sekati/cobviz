from __future__ import annotations
import requests
from typing import List, Dict, Optional
from .base import IntelligenceProvider
from .factory import ProviderRegistry

class OpenAICompatibleProvider(IntelligenceProvider):
    """
    Provider for OpenAI and any OpenAI-compatible API (vLLM, Groq, LM Studio, etc.)
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1", model: str = "gpt-3.5-turbo", **kwargs):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model

    def _request(self, prompt: str, system_message: str = "You are a helpful assistant.") -> str:
        # Security: Redact sensitive info before sending to cloud/enterprise
        prompt = self._sanitize_input(prompt)
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"Error from AI Provider: {str(e)}"

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Simplified for now, just uses the last message content
        return self._request(messages[-1]['content'])

    def summarize(self, text: str) -> str:
        return self._request(f"Summarize this code:\n\n{text}", "You are an expert software architect.")

    def explain(self, code: str, context: Optional[str] = None) -> str:
        prompt = f"Explain this code logic:\n\n{code}"
        if context:
            prompt += f"\n\nContext: {context}"
        return self._request(prompt, "You are a senior developer explaining legacy code.")

    def generateDocumentation(self, code: str) -> str:
        return self._request(f"Generate technical documentation for this code:\n\n{code}", "You are a technical writer.")

    def analyzeBusinessRules(self, code: str) -> str:
        return self._request(f"Extract business rules from this code:\n\n{code}", "You are a business analyst.")

    def impactAnalysis(self, code: str, change_description: str) -> str:
        return self._request(f"Analyze the impact of this change: {change_description}\n\nOn this code:\n\n{code}", "You are a risk manager.")

    def securityReview(self, code: str) -> str:
        return self._request(f"Perform a security review of this code:\n\n{code}", "You are a security engineer.")

# Register the providers
ProviderRegistry.register("openai", OpenAICompatibleProvider)
ProviderRegistry.register("enterprise", OpenAICompatibleProvider)
ProviderRegistry.register("cloud", OpenAICompatibleProvider)
ProviderRegistry.register("vllm", OpenAICompatibleProvider)
ProviderRegistry.register("groq", OpenAICompatibleProvider)
ProviderRegistry.register("lm-studio", OpenAICompatibleProvider)
