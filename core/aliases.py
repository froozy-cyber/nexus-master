# core/aliases.py
class Aliases:
    def __init__(self, learning_repo):
        self.learning_repo = learning_repo

    def resolve(self, text: str) -> str:
        aliases = self.learning_repo.get_aliases()

        for base, variants in aliases.items():
            for v in variants:
                if v in text:
                    return base
        return text
