# voice/audio.py - 🔥 АСИНХРОННЫЙ ЗВУК (НЕ БЛОКИРУЕТ!)
import sounddevice as sd
import soundfile as sf
import threading
import queue

class AudioPlayer:
    def __init__(self):
        self.play_queue = queue.Queue()

    def play(self, path: str):
        """🔥 ИГРАЕТ ФОНОМ - НЕ БЛОКИРУЕТ микрофон!"""
        def _play_async():
            try:
                data, samplerate = sf.read(path, dtype='float32')
                sd.play(data, samplerate)
                sd.wait()  # Только для этого звука
            except:
                pass
        
        # 🔥 ФОНОВЫЙ ПОТОК
        threading.Thread(target=_play_async, daemon=True).start()
