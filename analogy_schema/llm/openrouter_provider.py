import os
import json
import re
from typing import Type, TypeVar, Optional, Any, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from analogy_schema.llm.base import BaseLLMProvider

# Ensure .env is loaded
load_dotenv()

T = TypeVar("T", bound=BaseModel)


class OpenRouterProvider(BaseLLMProvider):
    """
    OpenRouter API provider supporting deepseek/deepseek-v4-flash with reasoning disabled.
    Handles structured output serialization and robust JSON parsing into Pydantic models.
    """

    def __init__(
        self,
        model_name: str = "deepseek/deepseek-v4-flash",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        disable_reasoning: bool = True,
    ):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment or .env file. Please check your .env configuration."
            )
        self.temperature = temperature
        self.disable_reasoning = disable_reasoning
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/analogy-schema",
                "X-Title": "Analogy Schema Induction Research",
            }
        )

    def _clean_json_text(self, text: str) -> str:
        """Extracts and cleans JSON string from model response."""
        text = text.strip()
        # Strip markdown ```json ... ``` code fences
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        return text

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        extra_body: Dict[str, Any] = {}
        if self.disable_reasoning:
            extra_body["reasoning"] = {"effort": "none"}

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            extra_body=extra_body if extra_body else None,
        )
        return response.choices[0].message.content or ""

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> T:
        schema_json = json.dumps(response_model.model_json_schema(), indent=2)
        schema_instruction = (
            f"\n\nIMPORTANT: You must output ONLY a valid JSON object strictly conforming to this JSON Schema:\n"
            f"```json\n{schema_json}\n```\n"
            f"Do not include any conversational preamble, commentary, or postscript outside the JSON."
        )

        full_prompt = prompt + schema_instruction
        system_content = (system_prompt or "You are a precise scientific NLP reasoning system.")

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": full_prompt},
        ]

        extra_body: Dict[str, Any] = {}
        if self.disable_reasoning:
            extra_body["reasoning"] = {"effort": "none"}

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=kwargs.get("temperature", self.temperature),
            extra_body=extra_body if extra_body else None,
        )

        raw_content = response.choices[0].message.content or "{}"
        cleaned_content = self._clean_json_text(raw_content)
        
        try:
            return response_model.model_validate_json(cleaned_content)
        except Exception as e:
            # Fallback parse via json.loads in case of typing quirks
            parsed_dict = json.loads(cleaned_content)
            return response_model.model_validate(parsed_dict)
