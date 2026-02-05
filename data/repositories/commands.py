# data/repositories/commands.py
from typing import Optional, List, Dict
from data.database import Database


class CommandsRepository:
    def __init__(self):
        self.db = Database.instance()

    def add(self, name: str, cmd_type: str, value: str) -> int:
        """
        Добавляет команду. Возвращает id добавленной команды.
        """
        self.db.execute(
            """
            INSERT OR IGNORE INTO commands (name, type, value)
            VALUES (?, ?, ?)
            """,
            (name.lower(), cmd_type, value)
        )
        # Получаем id только что добавленной команды
        row = self.get(name)
        if row:
            return row["id"]  # <-- предполагаем, что в БД есть автоинкремент 'id'
        return -1

    def get(self, name: str) -> Optional[Dict]:
        rows = self.db.query(
            "SELECT * FROM commands WHERE name = ?",
            (name.lower(),)
        )
        if not rows:
            return None
        return dict(rows[0])

    def all(self) -> List[Dict]:
        rows = self.db.query("SELECT * FROM commands")
        return [dict(r) for r in rows]

    def delete(self, name: str) -> None:
        self.db.execute(
            "DELETE FROM commands WHERE name = ?",
            (name.lower(),)
        )

    # --- Логика под старый код ---

    def exists(self, name: str) -> bool:
        return self.get(name) is not None

    def add_or_update(self, name: str, cmd_type: str, value: str) -> Dict:
        """
        Добавляет новую команду или обновляет существующую
        """
        name = name.lower()
    
        if self.exists(name):
            self.db.execute(
                """
                UPDATE commands
                SET type = ?, value = ?
                WHERE name = ?
                """,
                (cmd_type, value, name)
            )
        else:
            self.add(name, cmd_type, value)
    
        cmd = self.get(name)
        if cmd:
            return cmd
    
        return {"id": -1, "name": name, "type": cmd_type, "value": value}
    

    # Новый метод для assistant.py
    def get_by_name(self, name: str) -> Optional[Dict]:
        """Возвращает команду по имени"""
        return self.get(name)