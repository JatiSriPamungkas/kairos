import os
from dataclasses import dataclass

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    chunk_size: int = 512
    vad_threshold: float = 0.5
    silence_limit_sec: float = 0.6
    
@dataclass
class STTConfig:
    model_size: str = "base"
    language: str = "id"
    beam_size: int = 5

@dataclass
class VoiceModuleConfig:
    audio: AudioConfig = AudioConfig()
    stt: STTConfig = STTConfig()