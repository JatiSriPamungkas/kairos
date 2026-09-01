import numpy as np
import torch
from faster_whisper import WhisperModel
from .config import STTConfig, AudioConfig


class SpeechToText:
    def __init__(self, config: STTConfig = None):
        self.config = config or STTConfig()
        self.audio_config = AudioConfig()

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.compute_type = "float16" if self.device == "cuda" else "int8"

        print(
            f"[STT INIT] Memuat model Whisper '{self.config.model_size}' pada device: {self.device} ({self.compute_type})..."
        )

        self.model = WhisperModel(
            self.config.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

    def transcribe(self, audio_data: np.ndarray) -> str:
        if len(audio_data) < self.audio_config.sample_rate * 0.3:
            return ""

        segments, info = self.model.transcribe(
            audio_data,
            beam_size=self.config.beam_size,
            language=self.config.language,
            vad_filter=False,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            temperature=0.0,
            no_speech_threshold=0.6,
        )

        text_output = "".join([segment.text.strip() for segment in segments])
        return text_output