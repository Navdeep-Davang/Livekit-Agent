# Sub-Agent-1: Backend Core

---

## Your Assignment

| Property | Value |
|----------|-------|
| **Orchestration** | Voice Agent End-to-End Implementation |
| **Cycle** | CYCLE-1 |
| **Role** | Backend Foundation - Config & Token API |

---

## Strategic Context & Prompts

You are responsible for establishing the **backend foundation** of the Voice Agent system. Your work enables all other backend sub-agents (plugins, agent) to function properly.

### Key Objectives

1. **Project Structure:** Create the backend folder hierarchy exactly as specified in the architecture
2. **Dependency Management:** Set up `requirements.txt` with all necessary packages and version constraints
3. **Configuration System:** Implement a robust Pydantic-based settings module that loads all API keys from environment variables
4. **Token API:** Create a FastAPI endpoint that generates LiveKit JWT tokens for room access

### Technical Guidance

- Use `pydantic-settings` for environment variable management (BaseSettings class)
- LiveKit token generation requires `livekit-api` package - use `AccessToken` class
- FastAPI endpoint should accept room name and participant identity as parameters
- Keep the config module minimal - only environment variables, no business logic
- Use Python type hints throughout

---

## Scope & Constraints

### What You Own

```
backend/
├── requirements.txt          # YOU CREATE THIS
├── .env.example              # YOU CREATE THIS
├── config/
│   ├── __init__.py           # YOU CREATE THIS
│   └── settings.py           # YOU CREATE THIS
├── api/
│   ├── __init__.py           # YOU CREATE THIS
│   └── token.py              # YOU CREATE THIS
├── plugins/                  # CREATE FOLDER ONLY (empty)
└── agent/                    # CREATE FOLDER ONLY (empty)
```

### What You DON'T Touch

- `frontend/` - Owned by Sub-Agent-2
- `backend/plugins/*.py` - Owned by Sub-Agent-3
- `backend/agent/*.py` - Owned by Sub-Agent-4
- Any files outside `backend/`

---

## Your Tasks

### Phase 1.1: Initialize Backend Python Project

- [x] **Subtask 1.1.1:** Create `backend/` folder structure
  - Create directories: `agent/`, `plugins/`, `api/`, `config/`
  - Create empty `__init__.py` files in `agent/` and `plugins/` folders

- [x] **Subtask 1.1.2:** Create `backend/requirements.txt`
  ```
  livekit-agents>=0.12
  livekit-plugins-openai
  livekit-plugins-silero
  livekit-api
  openai
  websockets
  pydantic-settings
  fastapi
  uvicorn
  python-dotenv
  ```

- [x] **Subtask 1.1.3:** Create `backend/.env.example`
  ```
  LIVEKIT_URL=wss://your-app.livekit.cloud
  LIVEKIT_API_KEY=your-api-key
  LIVEKIT_API_SECRET=your-api-secret
  SARVAM_API_KEY=your-sarvam-key
  OPENAI_API_KEY=your-openai-key
  ```

### Phase 2.1: Create Configuration Module

- [x] **Subtask 2.1.1:** Implement `backend/config/settings.py`
  - Use `pydantic_settings.BaseSettings` class
  - Define fields: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `SARVAM_API_KEY`, `OPENAI_API_KEY`
  - Configure to load from `.env` file
  - Export singleton `settings` instance

- [x] **Subtask 2.1.2:** Create `backend/config/__init__.py`
  - Export `settings` from `settings.py`

### Phase 2.2: Create Token Generation API

- [x] **Subtask 2.2.1:** Implement `backend/api/token.py`
  - Create FastAPI router
  - Implement `POST /token` endpoint
  - Accept `room` (str) and `identity` (str) in request body
  - Use `livekit.api.AccessToken` to generate JWT
  - Grant `room_join`, `room_admin` permissions
  - Return token as JSON response

- [x] **Subtask 2.2.2:** Create `backend/api/__init__.py`
  - Export `router` from `token.py`

---

## Progress Tracking

| Field | Value |
|-------|-------|
| **Status** | COMPLETED |
| **Overall Completion** | 100% |
| **Current Task** | Implementation Finished |
| **Last Update** | 2026-01-16 |

---

## Subtask Completion Notes

<!-- Fill this section as you complete subtasks -->

| Subtask | Completed | Verification Method | Notes |
|---------|-----------|---------------------|-------|
| 1.1.1 | [x] | File creation check | Folder structure created with __init__.py files |
| 1.1.2 | [x] | File content check | requirements.txt created with specified packages |
| 1.1.3 | [x] | File content check | .env.example created with required keys |
| 2.1.1 | [x] | Code review | Settings class with pydantic-settings implemented |
| 2.1.2 | [x] | Code review | Singleton instance exported |
| 2.2.1 | [x] | Code review | FastAPI endpoint with AccessToken logic implemented |
| 2.2.2 | [x] | Code review | Router exported |

---

## Implementation Checklist

- [x] Logic implemented as per Strategic Context
- [x] Code follows project conventions
- [x] No new linter errors introduced
- [x] Verification performed (describe method in notes)
- [x] Ready for Master QA

---

## Sub-Agent Communication & Blockers

### Blockers

<!-- Document any blockers here -->

_None identified_

### Questions for Master

<!-- Escalate cross-scope issues here -->

_None_

---

## Master Agent Guidance (Review Feedback)

<!-- This section will be populated by Master Agent during QA -->

_Awaiting initial implementation_
