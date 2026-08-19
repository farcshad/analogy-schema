from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional, Any, Dict
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseLLMProvider(ABC):
    """Abstract interface for synchronous and asynchronous LLM calls with structured schema outputs."""

    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generates raw text response synchronously."""
        pass

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        """Generates validated structured output adhering to response_model synchronously."""
        pass

    @abstractmethod
    async def agenerate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generates raw text response asynchronously."""
        pass

    @abstractmethod
    async def agenerate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        """Generates validated structured output adhering to response_model asynchronously."""
        pass
