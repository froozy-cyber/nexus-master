# core/scorer.py
from typing import List, Tuple, Optional
from data.repositories.commands import CommandsRepository
from data.repositories.aliases import AliasesRepository
from data.repositories.learning import LearningRepository

class Scorer:
    def __init__(self):
        self.commands_repo = CommandsRepository()
        self.aliases_repo = AliasesRepository()
        self.learning_repo = LearningRepository()

    def score_phrase(self, phrase: str) -> List[Tuple[str, float]]:
        phrase = phrase.lower()
        words = phrase.split()

        results: List[Tuple[str, float]] = []

        for command in self.commands_repo.all():
            score = 0.0
            name = command["name"]

            # 1️⃣ Прямое вхождение имени команды
            if name in phrase:
                score += 5.0

            # 2️⃣ Частичное совпадение по словам
            for word in words:
                if word == name:
                    score += 3.0
                elif word in name or name in word:
                    score += 1.5

                # 3️⃣ Алиасы
                alias_cmd = self.aliases_repo.get_command_by_alias(word)
                if alias_cmd == name:
                    score += 4.0

            # 4️⃣ Обучение / confidence
            learned = self.learning_repo.get_confidence(phrase, name)
            score += learned * 2.0

            if score > 0:
                results.append((name, score))

        # сортировка по убыванию score
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def best_match(self, phrase: str) -> Optional[str]:
        results = self.score_phrase(phrase)
        if not results:
            return None
        return results[0][0]
