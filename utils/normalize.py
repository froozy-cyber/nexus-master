# utils/normalize.py
import re

def Normalize_Text(text: str) -> str:
    """
    Приведение текста к нижнему регистру, удаление лишних символов и пробелов
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # Убираем пунктуацию
    text = re.sub(r"\s+", " ", text).strip()
    return text
