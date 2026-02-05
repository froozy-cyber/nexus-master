#core/_utils.py
from fuzzywuzzy import fuzz
import re

STOP_WORDS = {"открой", "запусти", "покажи", "включи", "найди", "откройте", "запустите", "покажите", "пожалуйста", "мне"}

def normalize_word(word: str) -> str:
    word = word.lower()
    endings = ["у", "ю", "а", "я", "и", "ы", "е", "ё"]
    for e in endings:
        if word.endswith(e) and len(word) > 3:
            return word[:-len(e)] + "а"
    return word

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    words = [normalize_word(w) for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)

def is_sleep_command(text: str) -> bool:
    sleep_commands = ["спасибо", "отдыхай", "спи", "отдохни", "отдых", "спать", "поспи"]
    text_norm = normalize_text(text)
    for cmd in sleep_commands:
        if fuzz.ratio(cmd, text_norm) > 75 or cmd in text_norm:
            return True
    return False
