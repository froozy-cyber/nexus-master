# voice/controller.py
import logging
import os
import time

from voice.wake import WakeListener
from voice.stt import SpeechToText
from voice.audio import AudioPlayer
from config import VOICES_FOLDER

logger = logging.getLogger("VoiceController")


class VoiceController:
    def __init__(self, assistant):
        self.assistant = assistant
        self.audio = AudioPlayer()
        self.stt = SpeechToText()
        self.wake = None

        # 🔒 защита от повторного wake
        self.processing = False

    def start(self):
        if self.wake:
            return

        self.stt.start()
        self.wake = WakeListener(self.handle_wake, self.stt)
        self.wake.start()

        logger.info("🎤 VoiceController started")

    def handle_wake(self):
        if self.processing:
            return

        if self.assistant.state.state != "SLEEP":
            return

        self.processing = True

        try:
            logger.info("🎯 WAKE → LISTENING")

            self.assistant.state.set_state("LISTENING")
            self.assistant.events.emit("state_changed", "LISTENING")

            self.play_wake()
            time.sleep(0.1)

            self.stt.listening = True
            text = self.stt.listen(timeout_sec=4)
            self.stt.listening = False

            if text:
                logger.info(f"🎤 Распознано: {text}")
                result = self.assistant.handle_text_command(text)

                if result:
                    self.assistant.state.set_state("COMMAND")
                    self.assistant.events.emit("state_changed", "COMMAND")
                    self.play_random_command()
                    time.sleep(0.4)
                else:
                    self.play_not_found()
            else:
                logger.info("🔇 Тишина")
                self.play_not_found()

        except Exception as e:
            logger.exception(f"❌ Voice error: {e}")

        finally:
            self.assistant.state.set_state("SLEEP")
            self.assistant.events.emit("state_changed", "SLEEP")
            self.processing = False

    # ---------- AUDIO ----------

    def play_wake(self):
        self.audio.play(os.path.join(VOICES_FOLDER, "wake.wav"))

    def play_not_found(self):
        self.audio.play(os.path.join(VOICES_FOLDER, "not_found.wav"))

    def play_random_command(self):
        self.audio.play(os.path.join(VOICES_FOLDER, "command.wav"))

    def stop(self):
        if self.wake:
            self.wake.stop()
            self.wake = None
