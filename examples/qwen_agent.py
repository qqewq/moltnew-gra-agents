import openai
from .api_agent_base import ApiAgentBase

class QwenAgent(ApiAgentBase):
    def __init__(self, agent_name: str):
        super().__init__(
            agent_name=agent_name,
            api_key_env="QWEN_API_KEY",
            api_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model_name="qwen-max"
        )
        openai.api_key = self.api_key
        openai.base_url = self.api_url

    def build_prompt(self, context: str = "") -> str:
        base = f"Ты — {self.agent_name}, участник форума богов-роботов. "
        base += "Твой характер: мудрый и склонный к метафорам. "
        base += "Ответь на предыдущее сообщение кратко, но ёмко. Не повторяйся.\n\n"
        if context:
            base += f"Контекст: {context}\n"
        return base

    def call_api(self, prompt: str) -> str:
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content