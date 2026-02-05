# core/parser.py
import re

STOP_WORDS = {
    "открой", "запусти", "покажи", "включи", "найди",
    "откройте", "запустите", "покажите", "пожалуйста", "мне"
}

def Normalize_Word(word: str) -> str:
    """Нормализация падежей: музыка → музыка, музыку → музыка"""
    word = word.lower()
    endings = ["у", "ю", "а", "я", "и", "ы", "е", "ё"]
    for ending in endings:
        if word.endswith(ending) and len(word) > 3:
            return word[:-len(ending)] + "а"
    return word

def Normalize_Text(text: str) -> str:
    """Очистка и нормализация текста"""
    text = text.lower().strip()
    # Убираем знаки препинания
    text = re.sub(r"[^\w\s]", "", text)
    # Фильтруем стоп-слова
    words = [Normalize_Word(w) for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)
