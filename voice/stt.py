# voice/stt.py - 🔥 VOSK Готов мгновенно!
import json
import pyaudio
import threading
from vosk import Model, KaldiRecognizer
from config import VOSK_MODEL_PATH, SAMPLE_RATE, FRAMES_PER_BUFFER
import queue
import time

class SpeechToText:
    def __init__(self):
        print("🔄 Загрузка Vosk модели... (~2 сек)")
        self.model = Model(VOSK_MODEL_PATH)
        self.recognizer = None  # Будет готов при start()
        self.audio = None
        self.stream = None
        self.listening = False
        self.listening_queue = queue.Queue()
        self._preload_thread = None

    def preload(self):
        """🔥 ПРЕДЗАГРУЗКА PyAudio + Recognizer"""
        self.audio = pyaudio.PyAudio()
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
        print("✅ Vosk предзагружен!")

    def start(self):
        """🔥 Запуск фона"""
        if self._preload_thread is None:
            self._preload_thread = threading.Thread(target=self.preload, daemon=True)
            self._preload_thread.start()

    def listen(self, timeout_sec=5) -> str | None:
        """🔥 Слушает мгновенно (Vosk готов!)"""
        if not self.recognizer:
            time.sleep(0.1)  # Ждем предзагрузки
            if not self.recognizer:
                return None
                
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )
        
        frames = 0
        max_frames = timeout_sec * (SAMPLE_RATE // FRAMES_PER_BUFFER)
        
        while frames < max_frames and self.listening:
            try:
                data = self.stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    self._cleanup()
                    return text if text else None
            except:
                pass
            frames += 1
        
        self._cleanup()
        return None

    def _cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
