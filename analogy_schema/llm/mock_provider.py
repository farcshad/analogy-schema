import json
import asyncio
from typing import Type, TypeVar, Optional, Any, Dict, Callable
from pydantic import BaseModel
from analogy_schema.llm.base import BaseLLMProvider

T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic mock provider for unit tests and reproducible experiments.
    Supports both synchronous and asynchronous execution.
    """

    def __init__(self):
        self.registered_responses: Dict[str, Any] = {}
        self.call_history: list = []

    def register_response(self, stage_or_key: str, response: Any):
        """Registers a predefined output for a stage or keyword."""
        self.registered_responses[stage_or_key] = response

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        self.call_history.append({"prompt": prompt, "system_prompt": system_prompt, "type": "text"})
        for key, resp in self.registered_responses.items():
            if key in prompt or (system_prompt and key in system_prompt):
                if isinstance(resp, str):
                    return resp
                return json.dumps(resp)
        return "Mock text response"

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        self.call_history.append({
            "prompt": prompt,
            "system_prompt": system_prompt,
            "response_model": response_model.__name__,
            "type": "structured"
        })
        
        for key, resp in self.registered_responses.items():
            if key in prompt or (system_prompt and key in system_prompt) or key == response_model.__name__:
                if isinstance(resp, response_model):
                    return resp
                if isinstance(resp, dict):
                    return response_model.model_validate(resp)
                if isinstance(resp, str):
                    return response_model.model_validate_json(resp)
                if isinstance(resp, Callable):
                    result = resp(prompt, response_model)
                    if isinstance(result, response_model):
                        return result
                    return response_model.model_validate(result)

        raise ValueError(
            f"MockLLMProvider: No registered response found for model {response_model.__name__} in prompt: {prompt[:100]}..."
        )

    async def agenerate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return self.generate_text(prompt, system_prompt, **kwargs)

    async def agenerate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        return self.generate_structured(prompt, response_model, system_prompt, **kwargs)
