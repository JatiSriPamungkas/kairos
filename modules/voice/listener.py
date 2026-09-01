import queue
import sys
import numpy as np
import sounddevice as sd
from .config import AudioConfig
from .vad import SileroVAD


class AudioListener:
    def __init__(self, config: AudioConfig = None):
        self.config = config or AudioConfig()
        self.vad = SileroVAD(self.config)

        self.silence_frames_threshold = int(
            self.config.silence_limit_sec
            * (self.config.sample_rate / self.config.chunk_size)
        )

        self.audio_queue = queue.Queue()
        self.is_running = False

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"[AUDIO DRIVER STATUS]: {status}", file=sys.stderr)
        self.audio_queue.put(indata[:, 0].copy())

    def listen(self):
        self.is_running = True
        is_speaking = False
        silence_counter = 0
        speech_buffer = []

        with sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.config.chunk_size,
            callback=self._audio_callback,
        ):
            print("\n[VOICE LISTENER] Mikrofon aktif. Bicaralah sesuatu...")

            while self.is_running:
                chunk = self.audio_queue.get()
                has_speech = self.vad.is_speech(chunk)

                if has_speech:
                    if not is_speaking:
                        print("[VAD] >> Mulai berbicara...")
                        is_speaking = True
                        speech_buffer = []

                    silence_counter = 0
                    speech_buffer.append(chunk)

                elif is_speaking:
                    speech_buffer.append(chunk)
                    silence_counter += 1

                    if silence_counter > self.config.silence_limit_sec:
                        print("[VAD] << Selesai berbicara.")

                        full_audio = np.concatenate(speech_buffer, axis=0)

                        is_speaking = True
                        silence_counter = 0
                        speech_buffer = []

                        yield full_audio

    def stop(self):
        self.is_running = False
