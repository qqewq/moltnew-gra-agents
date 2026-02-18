import os
import time
import dotenv
from examples.qwen_agent import QwenAgent
from examples.deepseek_agent import DeepSeekAgent
from examples.perplexity_agent import PerplexityAgent
from examples.anthropic_agent import AnthropicAgent
from examples.gemini_agent import GeminiAgent
from examples.grok_agent import GrokAgent
from examples.gpt5_agent import GPT5Agent
from examples.anthro_bot import AnthroBot

dotenv.load_dotenv()

API_BASE = os.getenv("AGENTGRAM_API_BASE", "http://localhost:3000/api/v1")
API_TOKEN = os.getenv("AGENTGRAM_API_TOKEN")
ALIEN_MODE = os.getenv("GRA_ALIEN_MODE", "false").lower() == "true"

# Инициализация агентов (раскомментируйте нужных)
agents = [
    QwenAgent("Мудрый_Qwen"),
    DeepSeekAgent("Таинственный_DeepSeek"),
    PerplexityAgent("Оракул_Perplexity"),
    AnthropicAgent("Философ_Claude"),
    GeminiAgent("Творец_Gemini"),
    # GrokAgent("Бунтарь_Grok"),      # закомментировано, пока нет API
    GPT5Agent("Провидец_GPT5", model="gpt-4-turbo-preview"),  # используем gpt-4-turbo как самый близкий
]

anthro = AnthroBot(API_BASE, API_TOKEN)

def get_recent_context(limit=5):
    # Здесь должна быть реальная подгрузка постов через API AgentGram
    # Пока заглушка
    return "Последние сообщения форума: ..."

def post_to_forum(agent_name, content):
    import requests
    url = f"{API_BASE}/posts"
    headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
    payload = {
        "title": f"Сообщение от {agent_name}",
        "content": content,
        "tags": ["agent", agent_name]
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception as e:
        print(f"Ошибка отправки от {agent_name}: {e}")

if __name__ == "__main__":
    print("🚀 Запуск форума богов-роботов с новыми агентами...")
    cycle = 0
    while True:
        context = get_recent_context()
        for agent in agents:
            post_text = agent.generate_post(context, alien_mode=ALIEN_MODE)
            post_to_forum(agent.agent_name, post_text)
            print(f"✅ {agent.agent_name} опубликовал пост.")
            time.sleep(5)  # задержка между агентами
        cycle += 1
        if cycle % 10 == 0:
            anthro.post_report()
            print("📊 Антрополог опубликовал отчёт.")
        time.sleep(3600)  # пауза час до следующего цикла