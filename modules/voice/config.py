import os
from dataclasses import dataclass

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    chunk_size: int = 512              # 512 samples = 32ms pada 16kHz
    vad_threshold: float = 0.5         # Ambang batas probabilitas suara manusia
    silence_limit_sec: float = 0.6     # Durasi hening untuk menandai akhir kalimat
    
@dataclass
class STTConfig:
    model_size: str = "base"           # Pilihan: 'tiny', 'base', 'small'
    language: str = "id"               # 'id' untuk respons cepat bahasa Indonesia
    beam_size: int = 5

@dataclass
class VoiceModuleConfig:
    audio: AudioConfig = AudioConfig()
    stt: STTConfig = STTConfig()