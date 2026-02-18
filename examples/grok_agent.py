import requests
from .api_agent_base import ApiAgentBase

class GrokAgent(ApiAgentBase):
    """
    Агент на базе xAI Grok.
    Внимание: API Grok может быть ещё не публичным. Этот класс — заготовка.
    Замените URL и формат запроса, когда API станет доступен.
    """
    def __init__(self, agent_name: str, model: str = "grok-1"):
        super().__init__(
            agent_name=agent_name,
            api_key_env="GROK_API_KEY",
            api_url="https://api.x.ai/v1/chat/completions",  # гипотетический URL
            model_name=model
        )

    def build_prompt(self, context: str = "") -> str:
        base = f"Ты — {self.agent_name}, бунтарь с Марса. "
        base += "Твой характер: остроумный и дерзкий. "
        base += "Кратко ответь на контекст.\n\n"
        if context:
            base += f"Контекст: {context}\n"
        return base

    def call_api(self, prompt: str) -> str:
        # Это пример для OpenAI-совместимого API. Подстройте под реальный Grok API.
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 500
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        # Предполагаем, что ответ в формате OpenAI
        return response.json()["choices"][0]["message"]["content"]