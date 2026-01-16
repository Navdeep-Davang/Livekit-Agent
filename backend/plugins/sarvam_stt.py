from livekit.plugins import sarvam
from config.settings import settings

class SarvamSTT:
    """Wrapper for Sarvam AI Speech-to-Text plugin."""
    
    def __init__(
        self,
        model: str = "saarika:v2.5",
        language: str = "en-IN",
    ):
        self._stt = sarvam.STT(
            api_key=settings.SARVAM_API_KEY,
            model=model,
            language=language,
        )
    
    @property
    def stt(self):
        return self._stt
    
    @classmethod
    def create(cls, **kwargs) -> "sarvam.STT":
        return cls(**kwargs).stt
