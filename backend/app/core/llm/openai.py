from typing import Optional, Dict, Any
from openai import OpenAI
from .base import LLMBase, LLMResponse
from app.core.config import get_settings

settings = get_settings()

class OpenAILLM(LLMBase):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4"  # or gpt-3.5-turbo for lower cost
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        content: str = "",
        **kwargs
    ) -> LLMResponse:
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user content and prompt
            messages.append({
                "role": "user",
                "content": f"{content}\n\nPrompt: {prompt}"
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                meta_info={
                    "model": self.model,
                    "provider": "openai",
                    "finish_reason": response.choices[0].finish_reason,
                }
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")