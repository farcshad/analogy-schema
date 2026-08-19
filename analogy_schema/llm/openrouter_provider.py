import os
import json
import re
import asyncio
from typing import Type, TypeVar, Optional, Any, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI, AsyncOpenAI
from analogy_schema.llm.base import BaseLLMProvider

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class OpenRouterProvider(BaseLLMProvider):
    """
    Asynchronous and synchronous OpenRouter API provider supporting deepseek/deepseek-v4-flash
    with reasoning disabled and concurrent throughput.
    """

    def __init__(
        self,
        model_name: str = "deepseek/deepseek-v4-flash",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        disable_reasoning: bool = True,
        max_retries: int = 3,
        timeout: float = 60.0,
    ):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment or .env file. Please check your .env configuration."
            )
        self.temperature = temperature
        self.disable_reasoning = disable_reasoning
        self.max_retries = max_retries
        self.timeout = timeout
        
        headers = {
            "HTTP-Referer": "https://github.com/analogy-schema",
            "X-Title": "Analogy Schema Induction Research",
        }
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers=headers,
            timeout=self.timeout,
        )
        
        self.async_client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers=headers,
            timeout=self.timeout,
        )

    def _clean_json_text(self, text: str) -> str:
        """Extracts and cleans JSON string from model response."""
        text = text.strip()
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
        except Exception:
            parsed_dict = json.loads(cleaned_content)
            return response_model.model_validate(parsed_dict)

    async def agenerate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        extra_body: Dict[str, Any] = {}
        if self.disable_reasoning:
            extra_body["reasoning"] = {"effort": "none"}

        for attempt in range(self.max_retries):
            try:
                response = await self.async_client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=kwargs.get("temperature", self.temperature),
                    extra_body=extra_body if extra_body else None,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(1.0 * (attempt + 1))

    async def agenerate_structured(
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

        for attempt in range(self.max_retries):
            try:
                response = await self.async_client.chat.completions.create(
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
                except Exception:
                    parsed_dict = json.loads(cleaned_content)
                    return response_model.model_validate(parsed_dict)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(1.0 * (attempt + 1))
