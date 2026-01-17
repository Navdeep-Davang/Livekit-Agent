# Action Plan: Voice Agent End-to-End Implementation

Based on [voice-agent-architecture.md](../Architecture/voice-agent-architecture.md), this plan covers building a complete real-time voice assistant using LiveKit Agents framework with Sarvam AI (STT/TTS) and OpenAI GPT-5 mini.

---

## Phase 1: Project Setup and Configuration

Initialize both backend and frontend projects with proper dependency management and environment configuration.

- [x] **Task 1.1:** Initialize Backend Python Project
  - [x] Create `backend/` folder structure (`agent/`, `plugins/`, `api/`, `config/`)
  - [x] Create `requirements.txt` with dependencies (livekit-agents, livekit-plugins-openai, livekit-plugins-silero, websockets, pydantic-settings, fastapi, uvicorn)
  - [x] Create `.env.example` with required variables (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SARVAM_API_KEY, OPENAI_API_KEY)

- [x] **Task 1.2:** Initialize Frontend Next.js Project
  - [x] Create Next.js app in `frontend/` with TypeScript
  - [x] Install dependencies (@livekit/components-react, livekit-client)
  - [x] Create `.env.local.example` with required variables (NEXT_PUBLIC_LIVEKIT_URL, NEXT_PUBLIC_BACKEND_URL)

---

## Phase 2: Backend - Configuration and Token API

Set up the foundation for backend services.

- [x] **Task 2.1:** Create Configuration Module
  - [x] Implement `config/settings.py` with Pydantic BaseSettings for environment variables
  - [x] Create `config/__init__.py` for exports

- [x] **Task 2.2:** Create Token Generation API
  - [x] Implement `api/token.py` with FastAPI endpoint for LiveKit JWT token generation
  - [x] Create `api/__init__.py` for exports

---

## Phase 3: Backend - Sarvam AI Plugins

<!-- IMPLEMENTATION NOTE (2026-01-17):
The original plan called for custom WebSocket implementations for Sarvam STT/TTS.
Instead, we leveraged the official `livekit-plugins-sarvam` package which provides
production-ready integrations. This approach is more maintainable and follows
LiveKit best practices. The wrapper classes in plugins/ provide a clean interface
while delegating to the official plugin under the hood. -->

Implement custom STT and TTS plugins for Sarvam AI WebSocket integration.

- [x] **Task 3.1:** Implement Sarvam STT Plugin
  - [x] Create `plugins/sarvam_stt.py` implementing `livekit.agents.stt.STT` interface
  <!-- Subtasks below implemented via livekit-plugins-sarvam wrapper -->
  - [x] ~~Handle WebSocket streaming connection to Sarvam STT API~~ *(Handled by livekit-plugins-sarvam)*
  - [x] ~~Implement audio-to-text conversion with proper event handling~~ *(Handled by livekit-plugins-sarvam)*

- [x] **Task 3.2:** Implement Sarvam TTS Plugin
  - [x] Create `plugins/sarvam_tts.py` implementing `livekit.agents.tts.TTS` interface
  <!-- Subtasks below implemented via livekit-plugins-sarvam wrapper -->
  - [x] ~~Handle WebSocket streaming connection to Sarvam TTS API~~ *(Handled by livekit-plugins-sarvam)*
  - [x] ~~Implement text-to-audio conversion with proper streaming output~~ *(Handled by livekit-plugins-sarvam)*

- [x] **Task 3.3:** Create Plugin Module Exports
  - [x] Create `plugins/__init__.py` exporting both plugins

---

## Phase 4: Backend - Voice Pipeline Agent

Set up the main agent that orchestrates the STT, LLM, TTS pipeline.

- [x] **Task 4.1:** Create System Prompts
  - [x] Implement `agent/prompts.py` with system prompts for GPT-5 mini conversation

- [x] **Task 4.2:** Implement Agent Entry Point
  - [x] Create `agent/main.py` with VoicePipelineAgent setup
  - [x] Configure Silero VAD for voice activity detection
  - [x] Wire up Sarvam STT, OpenAI LLM, and Sarvam TTS in pipeline
  - [x] Implement room connection and event handling

- [x] **Task 4.3:** Create Backend Entry and Server
  - [x] Create `agent/__init__.py` for exports
  - [x] Set up FastAPI app combining token API and agent startup

---

## Phase 5: Frontend - Core Setup and Token Integration

Set up Next.js app with LiveKit client configuration.

- [x] **Task 5.1:** Create LiveKit Client Configuration
  - [x] Implement `lib/livekit.ts` with client configuration utilities

- [x] **Task 5.2:** Create Token API Route
  - [x] Implement `app/api/token/route.ts` to proxy token requests to backend

- [x] **Task 5.3:** Set Up App Layout
  - [x] Configure `app/layout.tsx` with proper metadata and styling

---

## Phase 6: Frontend - Voice UI Components

Build the user interface components for voice interaction.

- [x] **Task 6.1:** Create Connection Status Component
  - [x] Implement `components/ConnectionStatus.tsx` showing connection state

- [x] **Task 6.2:** Create Audio Visualizer Component
  - [x] Implement `components/AudioVisualizer.tsx` for audio waveform display

- [x] **Task 6.3:** Create Voice Agent Component
  - [x] Implement `components/VoiceAgent.tsx` with mic control and LiveKit hooks
  - [x] Handle start/stop recording, connection management

- [x] **Task 6.4:** Create Main Voice UI Page
  - [x] Implement `app/page.tsx` integrating all components
  - [x] Handle token fetching and LiveKit room connection

---

## Phase 7: Integration and End-to-End Testing

Verify the complete flow works correctly.

- [x] **Task 7.1:** Backend Integration Test
  - [x] Verify agent connects to LiveKit and processes audio correctly
  - [x] Test STT/TTS plugins with Sarvam API

- [x] **Task 7.2:** Frontend-Backend Integration
  - [x] Test token generation flow
  - [x] Verify WebRTC audio streaming between frontend and agent

- [x] **Task 7.3:** End-to-End Voice Conversation Test
  - [x] Complete voice conversation cycle: speak, transcribe, LLM response, TTS playback

---

## Architecture Reference

```
User speaks → Frontend (WebRTC) → LiveKit Room → Agent
    ↓
Silero VAD detects speech
    ↓
Sarvam STT (WebSocket) → Text
    ↓
GPT-5 mini → Response text
    ↓
Sarvam TTS (WebSocket) → Audio
    ↓
LiveKit Room → Frontend (WebRTC) → User hears response
```

---

## Key Files Summary

| Path | Purpose |
|------|---------|
| `backend/config/settings.py` | Pydantic environment config |
| `backend/api/token.py` | LiveKit JWT token endpoint |
| `backend/plugins/sarvam_stt.py` | Sarvam STT plugin |
| `backend/plugins/sarvam_tts.py` | Sarvam TTS plugin |
| `backend/agent/prompts.py` | System prompts for LLM |
| `backend/agent/main.py` | VoicePipelineAgent setup |
| `frontend/lib/livekit.ts` | LiveKit client config |
| `frontend/components/VoiceAgent.tsx` | Main voice component |
| `frontend/components/AudioVisualizer.tsx` | Audio waveform display |
| `frontend/components/ConnectionStatus.tsx` | Connection state indicator |
| `frontend/app/api/token/route.ts` | Token proxy to backend |
| `frontend/app/page.tsx` | Voice UI page |

---

## Dependencies

### Backend (`requirements.txt`)
- livekit-agents>=0.12
- livekit-plugins-openai
- livekit-plugins-silero
- livekit-plugins-sarvam
- openai
- websockets
- pydantic-settings
- fastapi
- uvicorn

### Frontend (`package.json`)
- @livekit/components-react
- livekit-client
- next
- react

---

## Completion Status

**Status:** COMPLETED (2026-01-17)

All phases implemented and verified by Master Agent orchestration.
See: [Orchestration Workspace](../Workspace/voice-agent-orchestration/master-agent.md)
