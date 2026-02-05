# ui/tray.py
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PySide6.QtGui import QAction, QIcon
from typing import Optional

import sys
import os

class SystemTray:
    def __init__(self, window: QWidget, icon_path: Optional[str] = None):
        self.window = window

        # иконка трея
        self.icon = QIcon(icon_path) if icon_path and os.path.exists(icon_path) else QIcon()

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # меню трея
        self.menu = QMenu()
        
        show_action = QAction("Показать окно")
        show_action.triggered.connect(self.show_window)
        self.menu.addAction(show_action)

        exit_action = QAction("Выход")
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

        self.tray.setContextMenu(self.menu)

    def show_window(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def exit_app(self):
        QApplication.quit()
