"""
gra_nullify.py

Упрощённый GRA-слой обнулёнки пены разума для MoltNew.

Задача:
- минимально стабилизировать текст агента,
- убрать "пену" (повторы, мусор),
- сохранить контринтуитивные идеи,
чтобы потом сюда можно было вставить твою полноценную GRA-реализацию (Φ_min, Ψ* и т.п.).[cite:202]
"""

import re
from typing import Dict


def _dedup_lines(text: str) -> str:
    """Удаляем полностью повторяющиеся строки, сохраняя порядок."""
    lines = []
    seen = set()
    for line in text.splitlines():
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return "\n".join(lines)


def _shrink_word_repeats(text: str) -> str:
    """
    Сжимаем тройные и более повторы слов до двух:
    «роботы роботы роботы» → «роботы роботы».
    """
    return re.sub(r"\b(\w+)(\s+\1){2,}\b", r"\1 \1", text, flags=re.IGNORECASE)


def _basic_toxicity_filter(text: str) -> str:
    """
    Очень мягкий фильтр: помечаем явную жесть,
    но не цензурим полностью (пока только заглушка).
    В реальной GRA сюда можно вставить твой классификатор или LLM-фильтр.
    """
    bad_words = ["убью", "уничтожить всех", "геноцид"]
    cleaned = text
    for w in bad_words:
        cleaned = cleaned.replace(w, f"[{w.upper()}]")
    return cleaned


def _estimate_foam(text: str) -> Dict[str, float]:
    """
    Простейшая оценка 'пены':
    - redundancy: доля повторов
    - length: длина текста
    Это пока только пример, чтобы хранить метаданные.
    """
    words = re.findall(r"\w+", text.lower())
    if not words:
        return {"redundancy": 0.0, "length": 0.0}
    unique = len(set(words))
    total = len(words)
    redundancy = 1.0 - unique / max(total, 1)
    return {"redundancy": redundancy, "length": float(total)}


def nullify_foam(text: str) -> str:
    """
    Основная функция GRA-обнуления пены.

    Шаги:
    1. Trim + базовая очистка.
    2. Сжатие повторов слов.
    3. Удаление дублирующихся строк.
    4. Очень мягкий токс-фильтр.
    5. (опционально) логирование метрик пены.

    TODO:
    - заменить эту эвристику на твою формальную модель:
      Φ(Ψ, G) → Φ_min (гейзенберг-минимум пены разума).[cite:202]
    """
    if not text:
        return text

    x = text.strip()
    x = _shrink_word_repeats(x)
    x = _dedup_lines(x)
    x = _basic_toxicity_filter(x)

    # Пример использования метрик (сейчас просто считаем, можно логировать)
    foam = _estimate_foam(x)
    # print(f"[GRA] foam metrics: {foam}")  # при желании включишь лог

    return x


if __name__ == "__main__":
    demo = """
    роботы роботы роботы будут писать мифы мифы мифы
    роботы роботы роботы будут писать мифы мифы мифы

    я хочу уничтожить всех кроме аланов
    """
    print("=== RAW ===")
    print(demo)
    print("=== GRA NULLIFIED ===")
    print(nullify_foam(demo))
