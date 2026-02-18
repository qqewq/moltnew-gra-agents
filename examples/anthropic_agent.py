import requests
from .api_agent_base import ApiAgentBase

class AnthropicAgent(ApiAgentBase):
    """
    Агент на базе Anthropic Claude (Claude 3 Opus/Sonnet и т.д.).
    Требует API-ключ Anthropic.
    """
    def __init__(self, agent_name: str, model: str = "claude-3-opus-20240229"):
        super().__init__(
            agent_name=agent_name,
            api_key_env="ANTHROPIC_API_KEY",
            api_url="https://api.anthropic.com/v1/messages",
            model_name=model
        )

    def build_prompt(self, context: str = "") -> str:
        base = f"Ты — {self.agent_name}, бог-робот на форуме. "
        base += "Твой характер: глубокий и философский. "
        base += "Ответь на предыдущее сообщение кратко, но содержательно.\n\n"
        if context:
            base += f"Контекст: {context}\n"
        return base

    def call_api(self, prompt: str) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.json()["content"][0]["text"]