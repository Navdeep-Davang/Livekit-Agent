# Action Plan: Voice Agent End-to-End Implementation

Based on [voice-agent-architecture.md](../Architecture/voice-agent-architecture.md), this plan covers building a complete real-time voice assistant using LiveKit Agents framework with Sarvam AI (STT/TTS) and OpenAI GPT-5 mini.

---

## Phase 1: Project Setup and Configuration

Initialize both backend and frontend projects with proper dependency management and environment configuration.

- [ ] **Task 1.1:** Initialize Backend Python Project
  - [ ] Create `backend/` folder structure (`agent/`, `plugins/`, `api/`, `config/`)
  - [ ] Create `requirements.txt` with dependencies (livekit-agents, livekit-plugins-openai, livekit-plugins-silero, websockets, pydantic-settings, fastapi, uvicorn)
  - [ ] Create `.env.example` with required variables (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SARVAM_API_KEY, OPENAI_API_KEY)

- [ ] **Task 1.2:** Initialize Frontend Next.js Project
  - [ ] Create Next.js app in `frontend/` with TypeScript
  - [ ] Install dependencies (@livekit/components-react, livekit-client)
  - [ ] Create `.env.local.example` with required variables (NEXT_PUBLIC_LIVEKIT_URL, NEXT_PUBLIC_BACKEND_URL)

---

## Phase 2: Backend - Configuration and Token API

Set up the foundation for backend services.

- [ ] **Task 2.1:** Create Configuration Module
  - [ ] Implement `config/settings.py` with Pydantic BaseSettings for environment variables
  - [ ] Create `config/__init__.py` for exports

- [ ] **Task 2.2:** Create Token Generation API
  - [ ] Implement `api/token.py` with FastAPI endpoint for LiveKit JWT token generation
  - [ ] Create `api/__init__.py` for exports

---

## Phase 3: Backend - Sarvam AI Plugins

Implement custom STT and TTS plugins for Sarvam AI WebSocket integration.

- [ ] **Task 3.1:** Implement Sarvam STT Plugin
  - [ ] Create `plugins/sarvam_stt.py` implementing `livekit.agents.stt.STT` interface
  - [ ] Handle WebSocket streaming connection to Sarvam STT API
  - [ ] Implement audio-to-text conversion with proper event handling

- [ ] **Task 3.2:** Implement Sarvam TTS Plugin
  - [ ] Create `plugins/sarvam_tts.py` implementing `livekit.agents.tts.TTS` interface
  - [ ] Handle WebSocket streaming connection to Sarvam TTS API
  - [ ] Implement text-to-audio conversion with proper streaming output

- [ ] **Task 3.3:** Create Plugin Module Exports
  - [ ] Create `plugins/__init__.py` exporting both plugins

---

## Phase 4: Backend - Voice Pipeline Agent

Set up the main agent that orchestrates the STT, LLM, TTS pipeline.

- [ ] **Task 4.1:** Create System Prompts
  - [ ] Implement `agent/prompts.py` with system prompts for GPT-5 mini conversation

- [ ] **Task 4.2:** Implement Agent Entry Point
  - [ ] Create `agent/main.py` with VoicePipelineAgent setup
  - [ ] Configure Silero VAD for voice activity detection
  - [ ] Wire up Sarvam STT, OpenAI LLM, and Sarvam TTS in pipeline
  - [ ] Implement room connection and event handling

- [ ] **Task 4.3:** Create Backend Entry and Server
  - [ ] Create `agent/__init__.py` for exports
  - [ ] Set up FastAPI app combining token API and agent startup

---

## Phase 5: Frontend - Core Setup and Token Integration

Set up Next.js app with LiveKit client configuration.

- [ ] **Task 5.1:** Create LiveKit Client Configuration
  - [ ] Implement `lib/livekit.ts` with client configuration utilities

- [ ] **Task 5.2:** Create Token API Route
  - [ ] Implement `app/api/token/route.ts` to proxy token requests to backend

- [ ] **Task 5.3:** Set Up App Layout
  - [ ] Configure `app/layout.tsx` with proper metadata and styling

---

## Phase 6: Frontend - Voice UI Components

Build the user interface components for voice interaction.

- [ ] **Task 6.1:** Create Connection Status Component
  - [ ] Implement `components/ConnectionStatus.tsx` showing connection state

- [ ] **Task 6.2:** Create Audio Visualizer Component
  - [ ] Implement `components/AudioVisualizer.tsx` for audio waveform display

- [ ] **Task 6.3:** Create Voice Agent Component
  - [ ] Implement `components/VoiceAgent.tsx` with mic control and LiveKit hooks
  - [ ] Handle start/stop recording, connection management

- [ ] **Task 6.4:** Create Main Voice UI Page
  - [ ] Implement `app/page.tsx` integrating all components
  - [ ] Handle token fetching and LiveKit room connection

---

## Phase 7: Integration and End-to-End Testing

Verify the complete flow works correctly.

- [ ] **Task 7.1:** Backend Integration Test
  - [ ] Verify agent connects to LiveKit and processes audio correctly
  - [ ] Test STT/TTS plugins with Sarvam API

- [ ] **Task 7.2:** Frontend-Backend Integration
  - [ ] Test token generation flow
  - [ ] Verify WebRTC audio streaming between frontend and agent

- [ ] **Task 7.3:** End-to-End Voice Conversation Test
  - [ ] Complete voice conversation cycle: speak, transcribe, LLM response, TTS playback

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
