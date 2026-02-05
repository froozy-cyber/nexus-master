#config.py
import os
import sys

VERSION = "v0.7.0"
APP_NAME = "N.E.X.U.S."

APP_W = 684
APP_H = 850

WAKE_WORD = "nexus"
SAMPLE_RATE = 16000
CHANNELS = 1
FRAMES_PER_BUFFER = 512

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PICOVOICE_ACCESS_KEY = "YJNWv6i+3F+sUYyenZVZMflLAmLlCb3GdNFSCFJRiQ/IuGaxl07LSg=="

ROOT_DIR = resource_path("")
COMMANDS_FILE = resource_path("data/commands.json")
LEARNING_FILE = resource_path("data/learning.json")
LOG_FILE = resource_path("nexus.log")

WAKEWORD_PPN_PATH = resource_path("assets/model_ru/nexus.ppn")
VOSK_MODEL_PATH = resource_path("assets/model_ru/vosk-model-small-ru-0.22")
VOICES_FOLDER = resource_path("assets/voices")
ICONS_FOLDER = resource_path("assets/icons")

JARVIS_COLORS = {
    "bg": "#0a0e1a",
    "panel": "#0f172a",
    "glass": "rgba(15, 23, 42, 0.8)",
    "accent": "#3b82f6",
    "success": "#10b981",
    "warn": "#f59e0b",
    "text_main": "#f8fafc",
    "text_dim": "#94a3b8",
}

STATE_COLORS = {
    "SLEEP": "#64748b",
    "LISTENING": "#3b82f6",
    "AI_ANALYZE": "#8b5cf6",
    "SEARCH": "#f59e0b",
    "COMMAND": "#10b981",
}