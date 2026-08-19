import os
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from analogy_schema.llm.base import BaseLLMProvider

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider with structured outputs support (also compatible with Ollama/vLLM/OpenRouter)."""

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.0,
    ):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package is required to use OpenAIProvider. Install with `pip install openai`.")
        
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url
        self.temperature = temperature
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key or self.base_url else None

    def _ensure_client(self):
        if self.client is None:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key or os.environ.get("OPENAI_API_KEY", ""), base_url=self.base_url)

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        self._ensure_client()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
        )
        return response.choices[0].message.content or ""

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        self._ensure_client()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=messages,
            response_format=response_model,
            temperature=kwargs.get("temperature", self.temperature),
        )
        return completion.choices[0].message.parsed
