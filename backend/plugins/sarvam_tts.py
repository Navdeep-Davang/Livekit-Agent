from livekit.plugins import sarvam
from config.settings import settings

class SarvamTTS:
    """Wrapper for Sarvam AI Text-to-Speech plugin."""
    
    def __init__(
        self,
        model: str = "bulbul:v2",
        speaker: str = "anushka",
        target_language_code: str = "en-IN",
        pitch: float = 0.0,
        pace: float = 1.0,
        loudness: float = 1.0,
    ):
        self._tts = sarvam.TTS(
            api_key=settings.SARVAM_API_KEY,
            model=model,
            speaker=speaker,
            target_language_code=target_language_code,
            pitch=pitch,
            pace=pace,
            loudness=loudness,
        )
    
    @property
    def tts(self):
        return self._tts
    
    @classmethod
    def create(cls, **kwargs) -> "sarvam.TTS":
        return cls(**kwargs).tts
