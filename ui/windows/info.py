#ui/windows/info.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QPalette, QColor, QTextCursor
from config import JARVIS_COLORS

class InfoTab(QWidget):
    def __init__(self, bridge=None):
        super().__init__()
        self.bridge = bridge
        self.has_animated = False

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedSize(430, 600)
        self.text_edit.setStyleSheet(f"""
            background-color: {JARVIS_COLORS['panel']};
            color: {JARVIS_COLORS['text_main']};
            border: none;
            padding: 10px;
            border-radius: 10px;
        """)
        font = QFont()
        font.setPointSize(12)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)

        self.full_text = """N.E.X.U.S. v0.7.0

👨‍💻 РАЗРАБОТЧИК: FROOZ
📍 ХИМКИ, МОСКОВСКАЯ ОБЛАСТЬ

🔬 ОСОБЕННОСТИ:
• Porcupine Wake Word ✅
• Vosk STT (офлайн) ✅  
• FuzzyWuzzy ИИ-матчинг ✅
• Авто-поиск .exe файлов ✅
• Реал-тайм статистика ✅
• Обучение алиасов ✅

🎯 СТАТУС: ГОТОВ К ТЕСТИРОВАНИЮ"""
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._type_text)
        self.text_index = 0

    def start_animation(self):
        if self.has_animated:
            self.text_edit.setText(self.full_text)
            return
        self.has_animated = True
        self.text_edit.clear()
        self.text_index = 0
        interval = max(1, int(3000 / len(self.full_text)))
        self.timer.start(interval)

    def _type_text(self):
        if self.text_index < len(self.full_text):
            self.text_edit.insertPlainText(self.full_text[self.text_index])
            self.text_index += 1
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        else:
            self.timer.stop()
