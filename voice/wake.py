# voice/wake.py
import threading
import struct
import queue
import logging

import sounddevice as sd
import pvporcupine

from config import PICOVOICE_ACCESS_KEY, WAKEWORD_PPN_PATH

logger = logging.getLogger("WakeListener")


class WakeListener:
    def __init__(self, on_wake_callback, stt):
        self.on_wake_callback = on_wake_callback
        self.stt = stt

        self.running = False
        self.queue = queue.Queue()

        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keyword_paths=[WAKEWORD_PPN_PATH]
        )

        self.stream = None

    def start(self):
        if self.running:
            return

        self.running = True

        def audio_callback(indata, frames, time, status):
            if not self.running:
                return

            if self.stt.listening:
                return

            try:
                pcm = struct.unpack_from(
                    "h" * self.porcupine.frame_length,
                    indata
                )
                if self.porcupine.process(pcm) >= 0:
                    self.queue.put(True)
            except Exception as e:
                logger.debug(e)

        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.porcupine.sample_rate,
            blocksize=self.porcupine.frame_length,
            dtype="int16",
            callback=audio_callback
        )
        self.stream.start()

        threading.Thread(
            target=self._dispatch_loop,
            daemon=True
        ).start()

        logger.info("🎧 WakeListener started")

    def _dispatch_loop(self):
        while self.running:
            try:
                self.queue.get(timeout=0.1)
                if not self.stt.listening:
                    threading.Thread(
                        target=self.on_wake_callback,
                        daemon=True
                    ).start()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        logger.info("🛑 WakeListener stopped")
