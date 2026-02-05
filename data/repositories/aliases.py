# data/repositories/aliases.py
from typing import List, Optional
from data.database import Database
from data.repositories.commands import CommandsRepository


class AliasesRepository:
    def __init__(self):
        self.db = Database.instance()
        self.commands_repo = CommandsRepository()

    def add_alias(self, alias: str, command_name: str) -> None:
        command = self.commands_repo.get(command_name)
        if not command:
            raise ValueError(f"Команда '{command_name}' не существует")

        self.db.execute(
            """
            INSERT OR IGNORE INTO aliases (alias, command_id)
            VALUES (?, ?)
            """,
            (alias.lower(), command["id"])
        )

    def get_command_by_alias(self, alias: str) -> Optional[str]:
        row = self.db.fetchone(
            """
            SELECT c.name
            FROM aliases a
            JOIN commands c ON c.id = a.command_id
            WHERE a.alias = ?
            """,
            (alias.lower(),)
        )
        return row["name"] if row else None

    def get_aliases_for_command(self, command_name: str) -> List[str]:
        command = self.commands_repo.get(command_name)
        if not command:
            return []

        rows = self.db.query(
            """
            SELECT alias
            FROM aliases
            WHERE command_id = ?
            """,
            (command["id"],)
        )
        return [r["alias"] for r in rows]

    def all(self) -> List[dict]:
        rows = self.db.query(
            """
            SELECT a.alias, c.name AS command
            FROM aliases a
            JOIN commands c ON c.id = a.command_id
            """
        )
        return [
            {"alias": r["alias"], "command": r["command"]}
            for r in rows
        ]
