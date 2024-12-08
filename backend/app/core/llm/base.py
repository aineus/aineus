# backend/app/core/llm/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class BaseLLM(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate text based on prompt"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if LLM service is available"""
        pass
