# data/database.py
import sqlite3
import os
from typing import Optional

DEFAULT_DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "jarvis.db")
)


class Database:
    _instance: Optional["Database"] = None

    def __init__(self):
        self.conn = sqlite3.connect(
            DEFAULT_DB_PATH,
            check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self._init_schema()

    # -------- SINGLETON --------

    @classmethod
    def instance(cls) -> "Database":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # -------- SCHEMA --------

    def _init_schema(self):
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT NOT NULL,
                command_id INTEGER NOT NULL,
                FOREIGN KEY(command_id) REFERENCES commands(id)
            );

            CREATE TABLE IF NOT EXISTS phrases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS confidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase TEXT NOT NULL,
                command TEXT NOT NULL,
                score REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS command_stats (
                command TEXT PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS file_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                type TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS app_cache (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    # -------- HELPERS --------

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query: str, params: tuple = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def query(self, query: str, params: tuple = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
