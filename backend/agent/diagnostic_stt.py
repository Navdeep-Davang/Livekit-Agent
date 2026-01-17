"""Diagnostic wrapper for Sarvam STT to capture all events."""

import logging
from livekit.agents import stt
from livekit.plugins import sarvam

logger = logging.getLogger("stt-debug")
logger.setLevel(logging.DEBUG)


class DiagnosticSTT(stt.STT):
    """Wrapper around Sarvam STT that logs all events for debugging."""
    
    def __init__(self, **kwargs):
        self._inner = sarvam.STT(**kwargs)
        super().__init__(
            capabilities=self._inner.capabilities
        )
    
    @property
    def model(self) -> str:
        return self._inner.model
    
    @property
    def provider(self) -> str:
        return "DiagnosticSarvam"
    
    def stream(self, **kwargs):
        stream = self._inner.stream(**kwargs)
        return DiagnosticSpeechStream(stream)
    
    async def _recognize_impl(self, buffer, **kwargs):
        result = await self._inner._recognize_impl(buffer, **kwargs)
        logger.info(f"[STT RECOGNIZE] Result: {result}")
        return result


class DiagnosticSpeechStream(stt.SpeechStream):
    """Wrapper that logs all events from the speech stream."""
    
    def __init__(self, inner_stream):
        self._inner = inner_stream
        # Don't call super().__init__ - we're just delegating
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            event = await self._inner.__anext__()
            logger.info(f"[STT EVENT] Type: {event.type}, Alternatives: {[a.text for a in (event.alternatives or [])]}")
            return event
        except StopAsyncIteration:
            logger.info("[STT EVENT] Stream ended (StopAsyncIteration)")
            raise
        except Exception as e:
            logger.error(f"[STT ERROR] {type(e).__name__}: {e}")
            raise
    
    async def aclose(self):
        logger.info("[STT] Closing stream")
        await self._inner.aclose()
    
    def push_frame(self, frame):
        self._inner.push_frame(frame)
    
    def end_input(self):
        logger.info("[STT] end_input called")
        self._inner.end_input()
    
    @property
    def _event_ch(self):
        return self._inner._event_ch
    
    @property
    def _input_ch(self):
        return self._inner._input_ch
