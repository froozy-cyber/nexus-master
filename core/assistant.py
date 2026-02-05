# core/assistant.py
import sys
import os
import logging
import subprocess
import webbrowser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.scorer import Scorer
from core.finder import AppFinder
from core.aliases import Aliases
from core.state import StateManager
from core.events import EventManager
from core._utils import normalize_text
from data.repositories.commands import CommandsRepository
from data.repositories.learning import LearningRepository
from data.repositories.stats import StatsRepository
from voice.controller import VoiceController

logger = logging.getLogger("Assistant")


class Assistant:
    def __init__(self):
        self.commands_repo = CommandsRepository()
        self.learning_repo = LearningRepository()
        self.stats_repo = StatsRepository()
        self.aliases = Aliases(self.learning_repo)
        self.finder = AppFinder()

        self.state = StateManager()
        self.events = EventManager()
        self.voice = VoiceController(self)

        self.scorer = Scorer()
        logger.info("🧠 Assistant v0.7.1 initialized")

    # ================= INTERNAL HELPERS =================

    def _set_state(self, state: str):
        self.state.set_state(state)
        self.events.emit("state_changed", state)

    # ================= VOICE =================

    def start_voice(self):
        self.voice.start()

    def on_wakeword(self):
        self.voice.handle_wake()

    # ================= COMMAND HANDLING =================

    def handle_text_command(self, text: str):
        text_clean = normalize_text(text)
        aliased = self.aliases.resolve(text_clean)

        # ---------- DATABASE COMMAND ----------
        best_name = self.scorer.best_match(aliased)
        if best_name:
            cmd = self.commands_repo.get(best_name)
            if cmd and self.execute(cmd):
                self.stats_repo.increment(best_name)
                self._set_state("COMMAND")
                return best_name

        # ---------- AI ANALYZE ----------
        self._set_state("AI_ANALYZE")

        found = self.finder.find(aliased)

        # ---------- SEARCH ----------
        self._set_state("SEARCH")

        if found:
            subprocess.Popen(found, shell=True)

            # 🔥 ОБУЧЕНИЕ + LIVE UPDATE UI
            self.commands_repo.add_or_update(
                name=aliased,
                cmd_type="app",
                value=found
            )
            self.events.emit("commands_updated")

            self._set_state("COMMAND")
            return found

        # ---------- FAIL ----------
        self.voice.play_not_found()
        self._set_state("SLEEP")
        return None

    # ================= EXECUTE =================

    def execute(self, cmd_data: dict) -> bool:
        try:
            cmd_type = cmd_data.get("type")
            value = cmd_data.get("value", "")

            if cmd_type == "url" and value:
                webbrowser.open(value)
                return True

            if cmd_type == "app" and value:
                if os.path.exists(value):
                    subprocess.Popen(value, shell=True)
                    return True

                exe_path = self.finder.find(value)
                if exe_path:
                    subprocess.Popen(exe_path, shell=True)
                    return True

        except Exception as e:
            logger.error(f"❌ Execute error: {e}")

        return False
