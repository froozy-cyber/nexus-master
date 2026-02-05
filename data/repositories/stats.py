# data/repositories/stats.py
from data.database import Database

class StatsRepository:
    def __init__(self):
        self.db = Database()
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                command TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
        """)

    def increment(self, command_name: str):
        current = self.get(command_name)
        if current is None:
            self.db.execute("INSERT INTO stats (command, count) VALUES (?, ?)", (command_name, 1))
        else:
            self.db.execute("UPDATE stats SET count = ? WHERE command = ?", (current + 1, command_name))

    def get(self, command_name: str):
        row = self.db.fetchone("SELECT count FROM stats WHERE command = ?", (command_name,))
        return row[0] if row else None
