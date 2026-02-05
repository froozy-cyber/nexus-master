from PySide6.QtCore import QObject, Signal, Slot
from core.assistant import Assistant


class Bridge(QObject):
    commands_updated = Signal()
    state_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.assistant = Assistant()
        self.assistant.start_voice()

        # 🔥 подписка на события ядра
        self.assistant.events.on("state_changed", self._on_state_changed)
        self.assistant.events.on("commands_updated", self._on_commands_updated)

    def _on_state_changed(self, state: str):
        self.state_changed.emit(state)

    def _on_commands_updated(self):
        self.commands_updated.emit()

    # ---------- COMMANDS ----------

    def get_all_commands(self) -> list:
        return self.assistant.commands_repo.all()

    @Slot(str, str, str)
    def add_command(self, name: str, cmd_type: str, value: str):
        self.assistant.commands_repo.add_or_update(name, cmd_type, value)
        self.commands_updated.emit()

    @Slot(str)
    def delete_command(self, name: str):
        self.assistant.commands_repo.delete(name)
        self.commands_updated.emit()

    def handle_text_command(self, text: str):
        return self.assistant.handle_text_command(text)

    def subscribe_state(self, callback):
        self.state_changed.connect(callback)
