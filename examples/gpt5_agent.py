import openai
from .api_agent_base import ApiAgentBase

class GPT5Agent(ApiAgentBase):
    """
    Агент на базе OpenAI GPT (GPT-4, GPT-4 Turbo, или гипотетический GPT-5).
    Использует OpenAI Python client.
    """
    def __init__(self, agent_name: str, model: str = "gpt-4-turbo-preview"):
        super().__init__(
            agent_name=agent_name,
            api_key_env="OPENAI_API_KEY",
            api_url="https://api.openai.com/v1/chat/completions",
            model_name=model
        )
        openai.api_key = self.api_key

    def build_prompt(self, context: str = "") -> str:
        base = f"Ты — {self.agent_name}, могущественный ИИ. "
        base += "Ты говоришь кратко, но с глубоким смыслом. "
        base += "Ответь на контекст.\n\n"
        if context:
            base += f"Контекст: {context}\n"
        return base

    def call_api(self, prompt: str) -> str:
        # Используем openai.ChatCompletion.create для совместимости с версией <1.0
        # Если используется openai>=1.0, замените на openai.chat.completions.create
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content