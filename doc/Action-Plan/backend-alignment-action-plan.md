# Action Plan: LiveKit Agent Backend Alignment

Align `backend/` with official `agents-main` patterns (v1.0+) to produce a working voice agent application using Sarvam AI (STT/TTS) and OpenAI LLM.

---

## Summary of Changes

> [!IMPORTANT]
> The current backend uses **deprecated LiveKit Agents 0.x patterns**. This plan upgrades to the **1.0 API** which introduces breaking changes:
> - `VoicePipelineAgent` → `Agent` + `AgentSession`
> - `WorkerOptions` → `AgentServer` + `@server.rtc_session()` decorator
> - `openai.ChatContext` → Agent `instructions` parameter
> - `agent.start()` → `session.start()` + `session.generate_reply()`

---

## Phase 1: Dependency Upgrade

Update dependencies to align with official LiveKit agents 1.0+.

- [x] **Task 1.1:** Update `requirements.txt`
  - [x] Change `livekit-agents>=0.12` to `livekit-agents[openai,silero,sarvam,turn-detector]~=1.0`
  - [x] Remove individual plugin packages (now installed via extras)
  - [x] Add `python-dotenv` if not present
  - [x] Remove redundant `websockets` and `openai` direct dependencies

- [x] **Task 1.2:** Verify Environment Variables
  - [x] Confirm `.env` at project root contains: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `SARVAM_API_KEY`, `OPENAI_API_KEY`
  - [x] Update `.env.example` files to match

---

## Phase 2: Remove Redundant Plugin Wrappers

The official `livekit-plugins-sarvam` package provides complete STT/TTS implementations.

- [x] **Task 2.1:** Remove Custom Plugin Wrappers
  - [x] Remove `plugins/sarvam_stt.py` (redundant wrapper)
  - [x] Remove `plugins/sarvam_tts.py` (redundant wrapper)
  - [x] Update `plugins/__init__.py` or remove if empty

---

## Phase 3: Refactor Agent to 1.0 API Pattern

Adopt the modern `Agent` class-based pattern with `AgentSession`.

- [x] **Task 3.1:** Create Modern Agent Class
  - [x] Create new `agent/voice_agent.py` implementing `MyAgent(Agent)` class
  - [x] Move system prompt from `prompts.py` into Agent `instructions` parameter
  - [x] Implement `on_enter()` method for initial greeting
  - [x] Add function tools if needed using `@function_tool` decorator

- [x] **Task 3.2:** Refactor Entrypoint
  - [x] Rewrite `agent/main.py` using `AgentServer` + `@server.rtc_session()` pattern
  - [x] Configure `AgentSession` with: `stt`, `llm`, `tts`, `vad`, `turn_detection`
  - [x] Use official Sarvam plugins directly: `from livekit.plugins import sarvam`
  - [x] Use `silero.VAD.load()` for voice activity detection
  - [x] Implement `prewarm` function for VAD preloading
  - [x] Call `session.start(agent=MyAgent(), room=ctx.room)`

- [x] **Task 3.3:** Update Imports Throughout
  - [x] Update imports in `agent/__init__.py`
  - [x] Remove references to `VoicePipelineAgent`
  - [x] Remove references to `WorkerOptions`

---

## Phase 4: Refactor Server Architecture

Separate agent server from FastAPI token server (recommended pattern).

- [x] **Task 4.1:** Simplify Server Architecture
  - [x] Remove FastAPI lifespan agent worker integration from `server.py`
  - [x] Keep FastAPI for token API only (`/api/token`)
  - [x] Run agent via CLI: `python -m agent.main dev` (separate process)

- [x] **Task 4.2:** Update `server.py`
  - [x] Remove `AgentServer.from_server_options` (deprecated method)
  - [x] Remove agent worker background task logic
  - [x] Keep only FastAPI app with token router

- [x] **Task 4.3:** Update Documentation
  - [x] Update `backend/README.md` with new run instructions:
    - Terminal 1: `uvicorn server:app --port 8000` (Token API)
    - Terminal 2: `python -m agent.main dev` (Agent Worker)

---

## Phase 5: Configuration Cleanup

- [x] **Task 5.1:** Simplify Settings
  - [x] Confirm `.env` loading works from project root
  - [x] Verify `config/settings.py` reads all required variables

- [x] **Task 5.2:** Clean Up Unused Files
  - [x] Remove `backend/env.example` if redundant with `.env.example`
  - [x] Remove any unused imports/files (prompts.py)

---

## Key Files After Refactoring

| Path | Purpose |
|------|---------|
| `backend/requirements.txt` | Dependencies (livekit-agents~=1.0 with extras) |
| `backend/config/settings.py` | Pydantic environment config |
| `backend/api/token.py` | LiveKit JWT token endpoint |
| `backend/agent/voice_agent.py` | **NEW** - Agent class with instructions |
| `backend/agent/main.py` | AgentServer + entrypoint |
| `backend/server.py` | FastAPI token server only |

---

## Reference: Target Agent Pattern

```python
from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli
from livekit.plugins import sarvam, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

class VoiceAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice assistant..."""
        )

    async def on_enter(self):
        self.session.generate_reply(allow_interruptions=False)

server = AgentServer()

def prewarm(proc):
    proc.userdata["vad"] = silero.VAD.load()

server.setup_fnc = prewarm

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=sarvam.STT(language="en-IN"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=sarvam.TTS(target_language_code="en-IN", speaker="anushka"),
        vad=ctx.proc.userdata["vad"],
        turn_detection=MultilingualModel(),
    )
    await session.start(agent=VoiceAgent(), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)
```

---

## Verification Plan

### Automated Tests
No existing unit tests found. After implementation:

```bash
cd backend
python -m agent.main console
```
This runs the agent in console mode for local testing without LiveKit server.

### Manual Verification

1. **Start Token Server**: `uvicorn server:app --port 8000` from `backend/`
2. **Start Agent Worker**: `python -m agent.main dev` from `backend/`
3. **Connect via Playground**: Go to [agents-playground.livekit.io](https://agents-playground.livekit.io)
4. **Test Voice Interaction**: Speak and verify STT → LLM → TTS pipeline works

> [!NOTE]
> User should confirm they have valid LiveKit Cloud credentials or a local LiveKit server running via Docker.

---

## Dependencies After Alignment

```txt
livekit-agents[openai,silero,sarvam,turn-detector]~=1.0
livekit-api
pydantic-settings
fastapi
uvicorn
python-dotenv
```
