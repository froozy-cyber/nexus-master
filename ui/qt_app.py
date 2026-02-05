#ui/qt_app.py
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                              QVBoxLayout, QSystemTrayIcon, QMenu, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
import sys
from ui.windows.home import HomeTab
from ui.windows.commands import CommandsTab
from ui.windows.info import InfoTab
from ui.bridge import Bridge
from config import JARVIS_COLORS, APP_H, APP_W

class MainWindow(QMainWindow):
    def __init__(self, bridge: Bridge):
        super().__init__()
        self.bridge = bridge
        self.init_tray()
        self.init_ui()

    def init_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("assets/icons/sleep.ico"))
        self.tray.setToolTip("N.E.X.U.S. v0.7.0")
        
        tray_menu = QMenu()
        tray_menu.addAction("Развернуть", self.show)
        tray_menu.addAction("Выход", self.quit_app)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def quit_app(self):
        QApplication.quit()

    def init_ui(self):
        self.setWindowTitle("N.E.X.U.S. v0.7.1")
        self.setFixedSize(APP_W, APP_H)
    
        central = QWidget()
        central.setStyleSheet(f"background-color: {JARVIS_COLORS['bg']};")
        self.setCentralWidget(central)
    
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar {
                background-color: #0b0f1a;
            }
            
            QTabBar::tab {
                width: 200px;
                height: 42px;      /* ✅ БОЛЬШИЕ КНОПКИ */
                background-color: #0b0f1a;
                color: #cbd5f5;
                font-size: 15px;
                border: none;
                padding: 10px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #1e40af;
                color: white;
            }
            
            QTabBar::tab:hover {
                background-color: #1f2937;
            }
        """)
        
        self.home_tab = HomeTab(self.bridge)
        self.commands_tab = CommandsTab(self.bridge)
        self.info_tab = InfoTab(self.bridge)
    
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.commands_tab, "Commands") 
        self.tabs.addTab(self.info_tab, "Info")
    
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs)
    
        self.bridge.subscribe_state(self.home_tab.update_state)

    def on_tab_changed(self, index):
        if self.tabs.tabText(index) == "ℹ️":
            self.info_tab.start_animation()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage(
            "N.E.X.U.S.", 
            "Свернут в трей", 
            QSystemTrayIcon.MessageIcon.Information, 
            2000
        )

def run_app():
    app = QApplication(sys.argv)
    bridge = Bridge()
    window = MainWindow(bridge)
    window.show()
    sys.exit(app.exec())
