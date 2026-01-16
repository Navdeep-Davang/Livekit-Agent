# Sub-Agent-4: Voice Pipeline Agent

---

## Your Assignment

| Property | Value |
|----------|-------|
| **Orchestration** | Voice Agent End-to-End Implementation |
| **Cycle** | CYCLE-2 |
| **Role** | Backend - Voice Pipeline Agent Setup |

---

## Strategic Context & Prompts

You are responsible for implementing the **main Voice Pipeline Agent** that orchestrates the entire STT → LLM → TTS flow. This is the core of the voice assistant that connects to LiveKit rooms and processes voice conversations.

### Key Objectives

1. **System Prompts:** Create well-crafted prompts for GPT-5 mini that define the assistant's personality and behavior
2. **Agent Entry Point:** Implement the main agent that wires together VAD, STT, LLM, and TTS
3. **FastAPI Integration:** Create the application entry point combining token API and agent

### Technical Guidance

- **VoicePipelineAgent:** Use `livekit.agents.VoicePipelineAgent` for the main pipeline
- **VAD:** Use `livekit.plugins.silero.VAD` for voice activity detection
- **LLM:** Use `livekit.plugins.openai.LLM` with GPT-5 mini model
- **STT/TTS:** Import custom Sarvam plugins from `plugins/`

- **Agent Worker Pattern:**
  ```python
  from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
  
  async def entrypoint(ctx: JobContext):
      # Set up pipeline and connect to room
      pass
  
  if __name__ == "__main__":
      cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
  ```

- **System Prompt Design:**
  - Keep it concise but effective
  - Define the assistant's role and capabilities
  - Set conversation tone (friendly, professional, etc.)
  - Include any constraints or guidelines

### Architecture Flow

```
User Audio → Silero VAD → Sarvam STT → GPT-5 mini → Sarvam TTS → User
```

---

## Scope & Constraints

### What You Own

```
backend/agent/
├── __init__.py           # YOU CREATE THIS
├── main.py               # YOU CREATE THIS
└── prompts.py            # YOU CREATE THIS
```

### What You DON'T Touch

- `backend/config/` - Owned by Sub-Agent-1
- `backend/api/` - Owned by Sub-Agent-1
- `backend/plugins/` - Owned by Sub-Agent-3
- `frontend/` - Owned by Sub-Agent-2
- `backend/requirements.txt` - Owned by Sub-Agent-1

### Dependencies (From Other Sub-Agents)

You will import:
```python
# From Sub-Agent-1
from config.settings import settings

# From Sub-Agent-3
from plugins import SarvamSTT, SarvamTTS
```

---

## Your Tasks

### Phase 4.1: Create System Prompts

- [ ] **Subtask 4.1.1:** Implement `backend/agent/prompts.py`
  - Define `SYSTEM_PROMPT` constant
  - Create a well-crafted prompt for GPT-5 mini
  - Include:
    - Assistant identity and role
    - Conversation style guidelines
    - Response length preferences
    - Any domain-specific instructions

### Phase 4.2: Implement Agent Entry Point

- [ ] **Subtask 4.2.1:** Create `backend/agent/main.py` base structure
  - Import all required components (VAD, STT, LLM, TTS)
  - Import settings from config
  - Import prompts

- [ ] **Subtask 4.2.2:** Implement `entrypoint()` function
  - Accept `JobContext` parameter
  - Initialize Silero VAD
  - Initialize Sarvam STT with settings
  - Initialize OpenAI LLM with GPT-5 mini
  - Initialize Sarvam TTS with settings

- [ ] **Subtask 4.2.3:** Configure VoicePipelineAgent
  - Create `VoicePipelineAgent` instance
  - Wire STT, LLM, TTS components
  - Set system prompt from prompts.py
  - Configure turn detection settings

- [ ] **Subtask 4.2.4:** Implement room connection
  - Connect to LiveKit room via context
  - Subscribe to audio tracks
  - Start the agent pipeline
  - Handle disconnection gracefully

- [ ] **Subtask 4.2.5:** Add CLI entry point
  - Use `livekit.agents.cli.run_app()`
  - Configure `WorkerOptions` with entrypoint
  - Set proper worker name

### Phase 4.3: Create Backend Entry and Server

- [ ] **Subtask 4.3.1:** Create `backend/agent/__init__.py`
  - Export main entrypoint function
  - Export any other public APIs

- [ ] **Subtask 4.3.2:** Document how to run the agent
  - Add docstring explaining usage
  - Command: `python -m agent.main dev` or similar

---

## Progress Tracking

| Field | Value |
|-------|-------|
| **Status** | READY |
| **Overall Completion** | 0% |
| **Current Task** | - |
| **Last Update** | 2026-01-16 |
| **Blocked By** | Partial - Task 4.1 (prompts.py) can start immediately |

---

## Subtask Completion Notes

<!-- Fill this section as you complete subtasks -->

| Subtask | Completed | Verification Method | Notes |
|---------|-----------|---------------------|-------|
| 4.1.1 | [ ] | - | - |
| 4.2.1 | [ ] | - | - |
| 4.2.2 | [ ] | - | - |
| 4.2.3 | [ ] | - | - |
| 4.2.4 | [ ] | - | - |
| 4.2.5 | [ ] | - | - |
| 4.3.1 | [ ] | - | - |
| 4.3.2 | [ ] | - | - |

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

- **Sub-Agent-3 Dependency:** Tasks 4.2+ cannot complete until `plugins/sarvam_stt.py` and `plugins/sarvam_tts.py` exist
- ~~**Sub-Agent-1 Dependency:** Needs `config/settings.py` for API keys~~ **RESOLVED** - config available

### Questions for Master

<!-- Escalate cross-scope issues here -->

_None_

### Note on Partial Work

Task 4.1 (prompts.py) has **no dependencies** and can be completed immediately. However, Tasks 4.2 and 4.3 depend on plugins from Sub-Agent-3.

---

## Master Agent Guidance (Review Feedback)

<!-- This section will be populated by Master Agent during QA -->

**CYCLE-2 ACTIVATED (2026-01-16)**

CYCLE-1 has been completed and verified. You are now READY to execute.

**Available Dependencies:**
- `config/settings.py` is available with all API keys
- Import pattern: `from config.settings import settings`

**Execution Strategy:**
1. **Start immediately:** Task 4.1 (prompts.py) has NO dependencies
2. **Wait for Sub-Agent-3:** Tasks 4.2+ require plugins to be complete

**Recommended Approach:**
- Begin with `agent/prompts.py` right away
- Monitor Sub-Agent-3 progress
- Complete `agent/main.py` and `agent/__init__.py` after plugins are available

_Ready for implementation_
