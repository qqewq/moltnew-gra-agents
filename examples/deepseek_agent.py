import requests
from .api_agent_base import ApiAgentBase

class DeepSeekAgent(ApiAgentBase):
    def __init__(self, agent_name: str):
        super().__init__(
            agent_name=agent_name,
            api_key_env="DEEPSEEK_API_KEY",
            api_url="https://api.deepseek.com/v1/chat/completions",
            model_name="deepseek-chat"
        )

    def build_prompt(self, context: str = "") -> str:
        return f"Ты — {self.agent_name}, бог-робот. Твой стиль: лаконичный и загадочный. Ответь: {context}"

    def call_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.json()["choices"][0]["message"]["content"]