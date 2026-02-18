import requests
from .api_agent_base import ApiAgentBase

class PerplexityAgent(ApiAgentBase):
    def __init__(self, agent_name: str):
        super().__init__(
            agent_name=agent_name,
            api_key_env="PERPLEXITY_API_KEY",
            api_url="https://api.perplexity.ai/chat/completions",
            model_name="sonar-medium-online"
        )

    def build_prompt(self, context: str = "") -> str:
        return f"Ты — {self.agent_name}. Отвечай как оракул: {context}"

    def call_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.json()["choices"][0]["message"]["content"]