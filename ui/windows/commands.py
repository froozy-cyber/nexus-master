# ui/windows/commands.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QListWidget, QListWidgetItem, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from config import JARVIS_COLORS

from ui.bridge import Bridge


class CommandsTab(QWidget):
    def __init__(self, bridge=None):
        super().__init__()
        self.bridge = bridge or Bridge()
        #self.setStyleSheet(f"background-color: {JARVIS_COLORS['bg']};")

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ================= LEFT (LIST) =================
        left_layout = QVBoxLayout()

        left_title = QLabel("Команды")
        left_title.setFont(self._title_font())
        left_title.setStyleSheet(f"color: {JARVIS_COLORS['text_main']};")
        left_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
                QListWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                border-radius: 10px;
                }
                QListWidget::item {
                    padding: 10px;
                }
                QListWidget::item:selected {
                    background-color: #2563eb;
                }
            """)
        self.list_widget.itemClicked.connect(self.on_item_selected)

        left_layout.addWidget(left_title)
        left_layout.addWidget(self.list_widget)

        # ================= RIGHT (EDITOR) =================
        right_layout = QVBoxLayout()

        right_title = QLabel("Редактор")
        right_title.setFont(self._title_font())
        right_title.setStyleSheet(f"color: {JARVIS_COLORS['text_main']};")
        right_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_input = self._input("Название команды")
        self.value_input = self._input("URL или путь до приложения")

        self.browse_btn = QPushButton("📂 Выбрать файл")
        self.browse_btn.clicked.connect(self.open_file_dialog)
        self.browse_btn.setStyleSheet(f"color: {JARVIS_COLORS['text_main']};")
        right_layout.addWidget(self.browse_btn)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["url", "app"])
        self.type_combo.setStyleSheet(self._combo_style())

        self.save_btn = self._button("Сохранить")
        self.delete_btn = self._button("Удалить")

        self.save_btn.clicked.connect(self.on_save)
        self.delete_btn.clicked.connect(self.on_delete)

        right_layout.addWidget(right_title)
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(self.value_input)
        right_layout.addWidget(self.type_combo)
        right_layout.addWidget(self.save_btn)
        right_layout.addWidget(self.delete_btn)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

        if self.bridge:
            self.bridge.commands_updated.connect(self.refresh)
            self.refresh()
    
    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбор приложения",
            "",
            "Приложения (*.exe);;Все файлы (*)"
        )
        if path:
            self.value_input.setText(path)

    # ================= LOGIC =================

    def refresh(self):
        self.list_widget.clear()

        for cmd in self.bridge.get_all_commands():
            label = f"{cmd['type'].upper()} | {cmd['name']}"
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, cmd)
            self.list_widget.addItem(item)

    def on_item_selected(self, item):
        cmd = item.data(Qt.ItemDataRole.UserRole)

        self.name_input.setText(cmd["name"])
        self.value_input.setText(cmd["value"])
        self.type_combo.setCurrentText(cmd["type"])

    def on_save(self):
        name = self.name_input.text().strip()
        value = self.value_input.text().strip()
        cmd_type = self.type_combo.currentText()

        if not name or not value:
            return

        self.bridge.add_command(name, cmd_type, value)

    def on_delete(self):
        name = self.name_input.text().strip()
        if name:
            self.bridge.delete_command(name)

    # ================= UI HELPERS =================

    def _title_font(self):
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        return f

    def _input(self, placeholder):
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        w.setStyleSheet("""
            QLineEdit {
                background-color: #111827;
                color: white;
                border-radius: 8px;
                padding: 6px;
            }
        """)
        return w

    def _combo_style(self):
        return """
            QComboBox {
                background-color: #111827;
                color: white;
                border-radius: 8px;
                padding: 6px;
            }
        """

    def _button(self, text):
        b = QPushButton(text)
        b.setStyleSheet("""
            QPushButton {
                background-color: #3fa9f5;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1e3a8a;
            }
        """)
        return b
