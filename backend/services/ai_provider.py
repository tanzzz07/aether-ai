import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from backend.config import Settings

class AIProvider:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete_json(self, system: str, user: str, schema_hint: Any) -> dict[str, Any]:
        if self.settings.ai_provider == "openrouter":
            return await self._openrouter(system, user, schema_hint)
        if self.settings.ai_provider == "ollama":
            return await self._ollama(system, user, schema_hint)
        return {}

    async def stream_text(self, chunks: list[str]) -> AsyncIterator[str]:
        for chunk in chunks:
            yield chunk

    async def _openrouter(self, system: str, user: str, schema_hint: str) -> dict[str, Any]:
        if not self.settings.openrouter_api_key:
            return {}

        payload = {
            "model": self.settings.openrouter_model,
            "messages": [
                {"role": "system", "content": f"{system}\nReturn JSON matching: {schema_hint}"},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    async def _ollama(self, system: str, user: str, schema_hint: str) -> dict[str, Any]:
        payload = {
            "model": self.settings.ollama_model,
            "stream": False,
            "format": "json",
            "prompt": f"{system}\nReturn JSON matching: {schema_hint}\n\n{user}",
        }
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{self.settings.ollama_base_url}/api/generate", json=payload)
            response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))