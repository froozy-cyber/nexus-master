from typing import List, Optional, Dict
from data.database import Database


class LearningRepository:
    def __init__(self):
        self.db = Database.instance()

    # ---------- PHRASES ----------

    def add_phrase(self, phrase: str) -> None:
        self.db.execute(
            "INSERT INTO phrases (phrase) VALUES (?)",
            (phrase.lower(),)
        )

    def last_phrases(self, limit: int = 20) -> List[str]:
        rows = self.db.query(
            """
            SELECT phrase
            FROM phrases
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        return [r["phrase"] for r in rows]

    # ---------- ALIASES ----------

    def get_aliases(self) -> Dict[str, str]:
        rows = self.db.query(
            """
            SELECT a.alias, c.name AS command_name
            FROM aliases a
            JOIN commands c ON c.id = a.command_id
            """
        )

        return {
            r["alias"].lower(): r["command_name"].lower()
            for r in rows
        }

    # ---------- CONFIDENCE ----------

    def get_confidence(self, phrase: str, command: str) -> float:
        """
        Возвращает confidence для пары (phrase, command)
        """
        row = self.db.fetchone(
            """
            SELECT score
            FROM confidence
            WHERE phrase = ? AND command = ?
            """,
            (phrase.lower(), command.lower())
        )
        return row["score"] if row else 0.0

    def increase_confidence(
        self, phrase: str, command: str, delta: float = 1.0
    ) -> None:
        row = self.db.fetchone(
            """
            SELECT id, score
            FROM confidence
            WHERE phrase = ? AND command = ?
            """,
            (phrase.lower(), command.lower())
        )

        if row:
            self.db.execute(
                """
                UPDATE confidence
                SET score = ?
                WHERE id = ?
                """,
                (row["score"] + delta, row["id"])
            )
        else:
            self.db.execute(
                """
                INSERT INTO confidence (phrase, command, score)
                VALUES (?, ?, ?)
                """,
                (phrase.lower(), command.lower(), delta)
            )

    def best_command_for_phrase(self, phrase: str) -> Optional[str]:
        row = self.db.fetchone(
            """
            SELECT command
            FROM confidence
            WHERE phrase = ?
            ORDER BY score DESC
            LIMIT 1
            """,
            (phrase.lower(),)
        )
        return row["command"] if row else None
