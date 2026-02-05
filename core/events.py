# core/events.py
from typing import Callable, Dict, List


class EventManager:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, callback: Callable):
        self._listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, *args, **kwargs):
        for callback in self._listeners.get(event_name, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"[EventManager] Error in '{event_name}': {e}")
