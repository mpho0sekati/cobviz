from __future__ import annotations
from typing import Dict, Type, Optional
from .base import IntelligenceProvider

class ProviderRegistry:
    _providers: Dict[str, Type[IntelligenceProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_cls: Type[IntelligenceProvider]):
        cls._providers[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, name: str, **kwargs) -> IntelligenceProvider:
        provider_cls = cls._providers.get(name.lower())
        if not provider_cls:
            raise ValueError(f"Provider '{name}' not found in registry.")
        return provider_cls(**kwargs)

    @classmethod
    def list_providers(cls) -> list[str]:
        return list(cls._providers.keys())

def create_intelligence_provider(config: Dict[str, Any]) -> IntelligenceProvider:
    """
    Factory function to create a provider based on configuration.
    Example config: {"type": "openai", "api_key": "...", "model": "gpt-4"}
    """
    provider_type = config.get("type", "mock")
    return ProviderRegistry.get_provider(provider_type, **config)
