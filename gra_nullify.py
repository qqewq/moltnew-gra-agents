import re
import os
from collections import Counter
import numpy as np

# Простая эвристика для измерения "пены"
def entropy(s):
    """Энтропия Шеннона для символов"""
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum(p * np.log2(p) for p in prob)

def nullify_foam(text, alien_mode=False, threshold=0.7):
    """
    Очищает текст от пены.
    Если alien_mode=True, использует метрики, не привязанные к человеческому языку.
    """
    if not alien_mode:
        # Стандартный режим: удаляем повторяющиеся фразы, клише (заглушка)
        sentences = re.split(r'[.!?]+', text)
        unique = []
        seen = set()
        for s in sentences:
            s_clean = s.strip().lower()
            if s_clean and s_clean not in seen and len(s_clean.split()) > 2:
                seen.add(s_clean)
                unique.append(s)
        return '. '.join(unique) + ('.' if unique else '')
    else:
        # Режим инопланетных культур: оцениваем внутреннюю предсказуемость
        tokens = list(text)  # посимвольно для простоты
        if len(tokens) < 5:
            return text
        # Частоты пар символов
        pairs = [tokens[i]+tokens[i+1] for i in range(len(tokens)-1)]
        pair_counts = Counter(pairs)
        total_pairs = len(pairs)
        # Если какая-то пара слишком частая (> threshold) - это признак пены
        foam_pairs = {p for p, cnt in pair_counts.items() if cnt/total_pairs > threshold}
        # Удаляем участки вокруг этих пар (очень грубо)
        result = []
        i = 0
        while i < len(tokens)-1:
            if tokens[i]+tokens[i+1] in foam_pairs:
                i += 2  # пропускаем эту пару и следующий символ (упрощённо)
            else:
                result.append(tokens[i])
                i += 1
        if i == len(tokens)-1:
            result.append(tokens[-1])
        return ''.join(result)