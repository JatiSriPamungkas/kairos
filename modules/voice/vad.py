import torch
import numpy as numpy
from .config import AudioConfig

class SileroVAD:
    def __init__(self, config: AudioConfig = None):
        self.config = config or AudioConfig()
        self.model = self._load_model()

    def _load_model(self):
        model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False,
            onnx = False
        )
        model.eval()
        return model

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        if not isinstance(audio_chunk, torch.Tensor):
            tensor_chunk = torch.from_numpy(audio_chunk).float()
        else:
            tensor_chunk = audio_chunk.float()
    
    with torch.no_grad():
        speech_prob = self.model(tensor_chunk, self.config.sample_rate).item()
    
    return speech_prob > self.config.vad_threshold