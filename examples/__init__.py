# examples/__init__.py

# Базовый класс для всех агентов
from .base_agent import BaseAgent

# Динамические API-агенты с GRA-обнулёнкой
from .qwen_agent import QwenAgent
from .deepseek_agent import DeepSeekAgent
from .perplexity_agent import PerplexityAgent
from .anthropic_agent import AnthropicAgent
from .gemini_agent import GeminiAgent
from .grok_agent import GrokAgent
from .gpt5_agent import GPT5Agent

# Агент-антрополог (динамический анализ)
from .anthro_bot import AnthroBot

__all__ = [
    "BaseAgent",
    "QwenAgent",
    "DeepSeekAgent",
    "PerplexityAgent",
    "AnthropicAgent",
    "GeminiAgent",
    "GrokAgent",
    "GPT5Agent",
    "AnthroBot",
]