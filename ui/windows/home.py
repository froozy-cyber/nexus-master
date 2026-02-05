# ui/windows/home.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from config import JARVIS_COLORS, STATE_COLORS


STATE_MAP = {
    "SLEEP": ("💤 НЕКСУС СПИТ", STATE_COLORS["SLEEP"]),
    "LISTENING": ("🎤 СЛУШАЮ", STATE_COLORS["LISTENING"]),
    "COMMAND": ("⚡ ВЫПОЛНЯЮ КОМАНДУ", STATE_COLORS["COMMAND"]),
    "AI_ANALYZE": ("🧠 ИИ АНАЛИЗИРУЕТ", STATE_COLORS["AI_ANALYZE"]),
    "SEARCH": ("🔍 ИЩУ НА КОМПЬЮТЕРЕ", STATE_COLORS["SEARCH"]),
}


class HomeTab(QWidget):
    def __init__(self, bridge=None):
        super().__init__()
        self.bridge = bridge

        self.current_state = "SLEEP"
        self.dots = 0

        self.init_ui()

        # ---- TIMER FOR DOTS ----
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(400)

        if self.bridge:
            self.bridge.subscribe_state(self.update_state)

    def init_ui(self):
        self.setStyleSheet(f"background-color: {JARVIS_COLORS['bg']};")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # ---- STATE LABEL ----
        self.state_label = QLabel()
        state_font = QFont()
        state_font.setPointSize(28)
        state_font.setBold(True)
        self.state_label.setFont(state_font)
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---- TITLE ----
        self.title_label = QLabel("N.E.X.U.S.")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {JARVIS_COLORS['text_main']};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---- SUBTITLE ----
        self.subtitle_label = QLabel("Voice Assistant")
        sub_font = QFont()
        sub_font.setPointSize(14)
        self.subtitle_label.setFont(sub_font)
        self.subtitle_label.setStyleSheet(f"color: {JARVIS_COLORS['text_dim']};")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.state_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

        self.renderr()

    # ================= STATE =================

    def update_state(self, state: str):
        self.current_state = state
        self.dots = 0
        self.renderr()

    def animate(self):
        if self.current_state in ("AI_ANALYZE", "SEARCH"):
            self.dots = (self.dots + 1) % 4
            self.renderr()

    def renderr(self):
        text, color = STATE_MAP.get(
            self.current_state,
            (self.current_state, "#FFFFFF")
        )

        suffix = "." * self.dots if self.current_state in ("AI_ANALYZE", "SEARCH") else ""
        self.state_label.setText(text + suffix)
        self.state_label.setStyleSheet(f"color: {color};")
