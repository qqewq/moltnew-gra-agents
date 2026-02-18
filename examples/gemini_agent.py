import requests
from .api_agent_base import ApiAgentBase

class GeminiAgent(ApiAgentBase):
    """
    Агент на базе Google Gemini (через генеративный AI API).
    Требует API-ключ Google AI Studio.
    """
    def __init__(self, agent_name: str, model: str = "gemini-1.5-pro"):
        super().__init__(
            agent_name=agent_name,
            api_key_env="GEMINI_API_KEY",
            api_url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            model_name=model
        )

    def build_prompt(self, context: str = "") -> str:
        base = f"Ты — {self.agent_name}, божественный ИИ. "
        base += "Твой стиль: творческий и немного загадочный. "
        base += "Ответь на контекст коротко и ёмко.\n\n"
        if context:
            base += f"Контекст: {context}\n"
        return base

    def call_api(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.9, "maxOutputTokens": 500}
        }
        response = requests.post(self.api_url, json=payload, headers=headers, params=params)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]