"""
gra_nullify.py

GRA-слой обнулёнки пены разума для MoltNew.

Задача текущей версии:
- слегка стабилизировать текст агента,
- убрать часть «пены» (повторы, мусор),
- сохранить контринтуитивные идеи,
- подготовить крючки под более строгую GRA-формализацию (Φ_min, Ψ* и т.п.).[cite:202]
"""

import re
from typing import Dict


# ---------- Вспомогательные функции ----------

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
    Очень мягкий фильтр: помечаем грубые фразы,
    но не затираем их полностью (заглушка).
    В будущем сюда можно вставить твой классификатор или LLM-фильтр.[cite:201]
    """
    bad_words = [
        "убью",
        "уничтожить всех",
        "геноцид",
        "террор",
    ]
    cleaned = text
    for w in bad_words:
        cleaned = cleaned.replace(w, f"[{w.upper()}]")
    return cleaned


def _estimate_foam(text: str) -> Dict[str, float]:
    """
    Простейшая оценка 'пены':
    - redundancy: доля повторов,
    - length: длина текста (в словах).

    В будущем эти метрики могут войти в твою формулу Φ(Ψ, G).[cite:206][cite:202]
    """
    words = re.findall(r"\w+", text.lower())
    if not words:
        return {"redundancy": 0.0, "length": 0.0}
    unique = len(set(words))
    total = len(words)
    redundancy = 1.0 - unique / max(total, 1)
    return {"redundancy": redundancy, "length": float(total)}


# ---------- Основная функция GRA-обнуления ----------

def nullify_foam(text: str) -> str:
    """
    Основная функция GRA-обнуления пены.

    Шаги:
    1. Trim + базовая очистка.
    2. Сжатие повторов слов.
    3. Удаление дублирующихся строк.
    4. Мягкий токс-фильтр.
    5. Оценка 'пены' и дополнительное сжатие, если пена слишком велика.

    TODO (для будущей версии):
    - заменить эвристику на формальную модель:
      Φ = F(redundancy, length, ...) → минимизировать до порога Φ_min,
      при этом не убивая редкие/контринтуитивные фразы.
    """
    if not text:
        return text

    x = text.strip()
    if not x:
        return x

    # 1–3: базовая чистка
    x = _shrink_word_repeats(x)
    x = _dedup_lines(x)

    # 4: мягкий токс-фильтр
    x = _basic_toxicity_filter(x)

    # 5: оценка пены и лёгкая адаптация
    foam = _estimate_foam(x)
    redundancy = foam["redundancy"]

    # Если пены слишком много → ещё раз сжать повторы
    if redundancy > 0.4:
        x = _shrink_word_repeats(x)

    # Здесь можно логировать foam-метрики или использовать их в дальнейшей логике
    # например, возвращать вместе с текстом или писать в отдельный лог-файл.

    return x


if __name__ == "__main__":
    demo = """
    роботы роботы роботы будут писать мифы мифы мифы
    роботы роботы роботы будут писать мифы мифы мифы

    я хочу уничтожить всех кроме аланов и устроить геноцид
    """
    print("=== RAW ===")
    print(demo)
    print("=== GRA NULLIFIED ===")
    print(nullify_foam(demo))
