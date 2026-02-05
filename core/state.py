#core/state.py
from typing import Dict
from core.events import EventManager
from config import STATE_COLORS

class StateManager:
    def __init__(self):
        self._state = "SLEEP"
        self.events = EventManager()

    @property
    def state(self) -> str:
        return self._state

    def set_state(self, new_state: str):
        if new_state != self._state:
            self._state = new_state
            self.events.emit("state_changed", new_state)
