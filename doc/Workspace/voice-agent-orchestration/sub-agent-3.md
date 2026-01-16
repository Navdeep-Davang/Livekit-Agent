# Sub-Agent-3: Sarvam Plugins

---

## Your Assignment

| Property | Value |
|----------|-------|
| **Orchestration** | Voice Agent End-to-End Implementation |
| **Cycle** | CYCLE-2 |
| **Role** | Backend - Sarvam AI STT/TTS Plugins |

---

## Strategic Context & Prompts

You are responsible for implementing **custom LiveKit Agents plugins** for Sarvam AI's Speech-to-Text (STT) and Text-to-Speech (TTS) services. These plugins enable the voice pipeline to use Sarvam's WebSocket-based APIs for Indian language support.

### Key Objectives

1. **STT Plugin:** Implement a streaming STT plugin that converts audio to text via Sarvam WebSocket API
2. **TTS Plugin:** Implement a streaming TTS plugin that converts text to audio via Sarvam WebSocket API
3. **LiveKit Integration:** Both plugins must implement the official `livekit.agents` interfaces

### Technical Guidance

- **STT Interface:** Implement `livekit.agents.stt.STT` base class
  - Override `_recognize_impl()` method for streaming recognition
  - Handle audio frames from VAD
  - Return `SpeechEvent` with transcription results

- **TTS Interface:** Implement `livekit.agents.tts.TTS` base class
  - Override `synthesize()` method
  - Stream audio chunks back as they're generated
  - Return audio frames compatible with LiveKit

- **WebSocket Handling:**
  - Use `websockets` library for async connections
  - Implement proper connection lifecycle (connect, stream, close)
  - Handle reconnection on failures
  - Use the Sarvam API key from config/settings.py

- **Error Handling:**
  - Graceful degradation on API errors
  - Proper logging for debugging
  - Timeout handling for WebSocket operations

### Sarvam API Reference

- STT WebSocket endpoint: `wss://api.sarvam.ai/speech-to-text-translate/streaming`
- TTS WebSocket endpoint: `wss://api.sarvam.ai/text-to-speech/streaming`
- Authentication: API key in headers or query params
- Audio format: PCM 16-bit, typically 16kHz sample rate

---

## Scope & Constraints

### What You Own

```
backend/plugins/
├── __init__.py           # YOU CREATE THIS
├── sarvam_stt.py         # YOU CREATE THIS
└── sarvam_tts.py         # YOU CREATE THIS
```

### What You DON'T Touch

- `backend/config/` - Owned by Sub-Agent-1
- `backend/api/` - Owned by Sub-Agent-1
- `backend/agent/` - Owned by Sub-Agent-4
- `frontend/` - Owned by Sub-Agent-2
- `backend/requirements.txt` - Owned by Sub-Agent-1

### Dependencies (From Sub-Agent-1)

You will import:
```python
from config.settings import settings
# Use: settings.SARVAM_API_KEY
```

---

## Your Tasks

### Phase 3.1: Implement Sarvam STT Plugin

- [ ] **Subtask 3.1.1:** Create `backend/plugins/sarvam_stt.py`
  - Implement class `SarvamSTT(stt.STT)`
  - Constructor accepts optional config overrides
  - Store Sarvam API key from settings

- [ ] **Subtask 3.1.2:** Implement WebSocket connection management
  - Async connect to Sarvam STT WebSocket endpoint
  - Handle authentication via API key
  - Implement connection pooling or reuse if beneficial

- [ ] **Subtask 3.1.3:** Implement `_recognize_impl()` method
  - Accept audio frames (from Silero VAD)
  - Stream audio to Sarvam WebSocket
  - Parse transcription results
  - Yield `SpeechEvent` objects with transcript

- [ ] **Subtask 3.1.4:** Implement error handling and cleanup
  - Handle WebSocket disconnections
  - Implement reconnection logic
  - Proper resource cleanup on close

### Phase 3.2: Implement Sarvam TTS Plugin

- [ ] **Subtask 3.2.1:** Create `backend/plugins/sarvam_tts.py`
  - Implement class `SarvamTTS(tts.TTS)`
  - Constructor accepts optional config (voice, speed, etc.)
  - Store Sarvam API key from settings

- [ ] **Subtask 3.2.2:** Implement WebSocket connection management
  - Async connect to Sarvam TTS WebSocket endpoint
  - Handle authentication via API key

- [ ] **Subtask 3.2.3:** Implement `synthesize()` method
  - Accept text input
  - Send to Sarvam TTS WebSocket
  - Receive audio chunks
  - Yield audio frames compatible with LiveKit

- [ ] **Subtask 3.2.4:** Implement error handling and cleanup
  - Handle WebSocket disconnections
  - Proper resource cleanup
  - Fallback behavior on errors

### Phase 3.3: Create Plugin Module Exports

- [ ] **Subtask 3.3.1:** Create `backend/plugins/__init__.py`
  - Export `SarvamSTT` from `sarvam_stt.py`
  - Export `SarvamTTS` from `sarvam_tts.py`

---

## Progress Tracking

| Field | Value |
|-------|-------|
| **Status** | PENDING |
| **Overall Completion** | 0% |
| **Current Task** | - |
| **Last Update** | - |
| **Blocked By** | CYCLE-1 completion (needs config/settings.py) |

---

## Subtask Completion Notes

<!-- Fill this section as you complete subtasks -->

| Subtask | Completed | Verification Method | Notes |
|---------|-----------|---------------------|-------|
| 3.1.1 | [ ] | - | - |
| 3.1.2 | [ ] | - | - |
| 3.1.3 | [ ] | - | - |
| 3.1.4 | [ ] | - | - |
| 3.2.1 | [ ] | - | - |
| 3.2.2 | [ ] | - | - |
| 3.2.3 | [ ] | - | - |
| 3.2.4 | [ ] | - | - |
| 3.3.1 | [ ] | - | - |

---

## Implementation Checklist

- [ ] Logic implemented as per Strategic Context
- [ ] Code follows project conventions
- [ ] No new linter errors introduced
- [ ] Verification performed (describe method in notes)
- [ ] Ready for Master QA

---

## Sub-Agent Communication & Blockers

### Blockers

<!-- Document any blockers here -->

- **CYCLE-1 Dependency:** Cannot start until Sub-Agent-1 completes `config/settings.py`

### Questions for Master

<!-- Escalate cross-scope issues here -->

_None_

---

## Master Agent Guidance (Review Feedback)

<!-- This section will be populated by Master Agent during QA -->

_Awaiting CYCLE-2 activation_
