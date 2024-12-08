from typing import Dict, Type
from app.core.llm.base import BaseLLM
from app.core.config import get_settings  # This should now work

class LLMFactory:
    _adapters: Dict[str, Type[BaseLLM]] = {}
    
    @classmethod
    def register_adapter(cls, name: str, adapter: Type[BaseLLM]):
        """Register a new LLM adapter"""
        cls._adapters[name] = adapter
    
    @classmethod
    def create(cls, provider: str = None) -> BaseLLM:
        """Create an instance of the specified LLM adapter"""
        settings = get_settings()
        provider = provider or settings.LLM_PROVIDER
        
        if provider not in cls._adapters:
            raise ValueError(f"Unsupported LLM provider: {provider}")
            
        adapter_class = cls._adapters[provider]
        return adapter_class()

# Import and register adapters
# We'll add these implementations later
# from app.core.llm.openai import OpenAIAdapter
# from app.core.llm.llama import LlamaAdapter
# from app.core.llm.mistral import MistralAdapter

# LLMFactory.register_adapter("openai", OpenAIAdapter)
# LLMFactory.register_adapter("llama", LlamaAdapter)
# LLMFactory.register_adapter("mistral", MistralAdapter)