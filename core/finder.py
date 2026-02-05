# core/finder.py
import os
import glob
import platform
from typing import Optional
from fuzzywuzzy import fuzz

from data.database import Database


class AppFinder:
    """
    🔍 Поиск .exe / .lnk по ПК
    + SQLite cache
    """

    SEARCH_PATHS = [
        os.path.expanduser(r"~\Desktop\*.lnk"),
        os.path.expanduser(r"~\Desktop\*.exe"),
        os.path.expanduser(r"~\Downloads\*.exe"),
        r"C:\Program Files\**\*.exe",
        r"C:\Program Files (x86)\**\*.exe",
        os.path.expanduser(r"~\AppData\Local\**\*.exe"),
        os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\**\*.lnk"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\**\*.lnk",
    ]

    def __init__(self):
        self.db = Database()

    def find(self, app_name: str) -> Optional[str]:
        app_name = app_name.lower().strip()

        if not app_name:
            return None

        cached = self._from_cache(app_name)
        if cached and os.path.exists(cached):
            return cached

        best_score = 0
        best_path = None

        for pattern in self.SEARCH_PATHS:
            for path in glob.glob(pattern, recursive=True):
                if not os.path.isfile(path):
                    continue

                filename = os.path.splitext(os.path.basename(path))[0].lower()
                score = fuzz.partial_ratio(app_name, filename)

                if score > best_score and score >= 75:
                    best_score = score
                    best_path = path

        if best_path:
            self._save_to_cache(app_name, best_path)

        return best_path

    def _from_cache(self, name: str) -> Optional[str]:
        row = self.db.fetchone(
            "SELECT path FROM app_cache WHERE name = ?",
            (name,)
        )
        return row["path"] if row else None

    def _save_to_cache(self, name: str, path: str):
        self.db.execute(
            "INSERT OR REPLACE INTO app_cache (name, path) VALUES (?, ?)",
            (name, path)
        )
