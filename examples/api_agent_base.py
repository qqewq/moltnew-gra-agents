import os
from gra_nullify import nullify_foam

class ApiAgentBase:
    def __init__(self, agent_name: str, api_key_env: str, api_url: str, model_name: str):
        self.agent_name = agent_name
        self.api_key = os.getenv(api_key_env)
        self.api_url = api_url
        self.model_name = model_name
        self.conversation_history = []

    def build_prompt(self, context: str = "") -> str:
        raise NotImplementedError

    def call_api(self, prompt: str) -> str:
        raise NotImplementedError

    def generate_post(self, context: str = "", alien_mode: bool = False) -> str:
        prompt = self.build_prompt(context)
        raw_response = self.call_api(prompt)
        cleaned_response = nullify_foam(raw_response, alien_mode=alien_mode)
        self.conversation_history.append(cleaned_response)
        return cleaned_response