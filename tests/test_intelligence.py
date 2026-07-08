import pytest
from cobviz.intelligence.factory import ProviderRegistry, create_intelligence_provider
from cobviz.intelligence.mock_provider import MockProvider
from cobviz.intelligence.openai_provider import OpenAICompatibleProvider

def test_provider_registry():
    assert "mock" in ProviderRegistry.list_providers()
    assert "openai" in ProviderRegistry.list_providers()

    provider = ProviderRegistry.get_provider("mock")
    assert isinstance(provider, MockProvider)

def test_create_intelligence_provider_factory():
    config = {"type": "mock"}
    provider = create_intelligence_provider(config)
    assert isinstance(provider, MockProvider)

    config = {"type": "openai", "api_key": "test", "model": "gpt-4"}
    provider = create_intelligence_provider(config)
    assert isinstance(provider, OpenAICompatibleProvider)
    assert provider.api_key == "test"
    assert provider.model == "gpt-4"

def test_mock_provider_methods():
    provider = MockProvider()
    assert "mock response" in provider.chat([{"role": "user", "content": "hi"}])
    assert "Explanation" in provider.explain("MOVE A TO B")
    assert "Security Review" in provider.securityReview("...")
