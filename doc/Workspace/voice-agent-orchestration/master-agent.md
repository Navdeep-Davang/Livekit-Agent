# Master Agent: Voice Agent Orchestration

---

## Executive Summary

Building a complete real-time voice assistant using LiveKit Agents framework with Sarvam AI (STT/TTS) and OpenAI GPT-5 mini. The system enables voice conversations where users speak through a Next.js frontend, audio streams via WebRTC to a Python backend agent that processes speech through Silero VAD, Sarvam STT, GPT-5 mini LLM, and Sarvam TTS, returning synthesized audio responses.

---

## Source Reference

- **Architecture:** [voice-agent-architecture.md](../../Architecture/voice-agent-architecture.md)
- **Action Plan:** [voice-agent-action-plan.md](../../Action-Plan/voice-agent-action-plan.md)

---

## Orchestration Metadata

| Property | Value |
|----------|-------|
| **Feature Name** | Voice Agent End-to-End Implementation |
| **Total Phases** | 7 |
| **Total Tasks** | 17 |
| **Total Subtasks** | 28 |
| **Sub-Agents** | 4 |
| **Current Cycle** | CYCLE-2 |
| **Overall Completion** | 100% |
| **Status** | COMPLETED |

---

## Architecture & Constraints

### Dependency Map

```
Phase 1.1 (Backend Setup) ─┬─► Phase 2 (Config/Token) ─► Phase 3 (Plugins) ─► Phase 4 (Agent)
                           │
Phase 1.2 (Frontend Setup) ─► Phase 5 (Core Setup) ─► Phase 6 (UI Components)
                           │
                           └─────────────────────────────────────────────────► Phase 7 (Integration)
```

### Critical Constraints

1. **Backend Config First:** `config/settings.py` must exist before plugins can import settings
2. **Plugins Before Agent:** `plugins/` must be complete before `agent/main.py` can wire the pipeline
3. **Token API Required:** Both backend token endpoint and frontend proxy must work for LiveKit connection
4. **Zero File Overlap:** Each sub-agent owns distinct directories

---

## Current Distribution: CYCLE-2

| Sub-Agent | Phases | Status | Files Owned |
|-----------|--------|--------|-------------|
| **Sub-Agent-3** | 3 | READY | `backend/plugins/` |
| **Sub-Agent-4** | 4 | READY | `backend/agent/` |

### CYCLE-1 (Completed)

| Sub-Agent | Phases | Status | Files Owned |
|-----------|--------|--------|-------------|
| **Sub-Agent-1** | 1.1 + 2 | COMPLETED | `backend/config/`, `backend/api/`, `backend/requirements.txt`, `backend/.env.example` |
| **Sub-Agent-2** | 1.2 + 5 + 6 | COMPLETED | `frontend/` (entire directory) |

---

## Sub-Agent Status

| Sub-Agent | Assigned Cycle | Status | Completion | Last Update |
|-----------|----------------|--------|------------|-------------|
| Sub-Agent-1 | CYCLE-1 | COMPLETED | 100% | 2026-01-16 |
| Sub-Agent-2 | CYCLE-1 | COMPLETED | 100% | 2026-01-16 |
| Sub-Agent-3 | CYCLE-2 | COMPLETED | 100% | 2026-01-16 |
| Sub-Agent-4 | CYCLE-2 | COMPLETED | 100% | 2026-01-17 |

---

## Task Registry

### Phase 1: Project Setup and Configuration

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 1.1 | Initialize Backend Python Project | Sub-Agent-1 | COMPLETED |
| 1.2 | Initialize Frontend Next.js Project | Sub-Agent-2 | COMPLETED |

### Phase 2: Backend - Configuration and Token API

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 2.1 | Create Configuration Module | Sub-Agent-1 | COMPLETED |
| 2.2 | Create Token Generation API | Sub-Agent-1 | COMPLETED |

### Phase 3: Backend - Sarvam AI Plugins

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 3.1 | Implement Sarvam STT Plugin | Sub-Agent-3 | COMPLETED |
| 3.2 | Implement Sarvam TTS Plugin | Sub-Agent-3 | COMPLETED |
| 3.3 | Create Plugin Module Exports | Sub-Agent-3 | COMPLETED |

### Phase 4: Backend - Voice Pipeline Agent

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 4.1 | Create System Prompts | Sub-Agent-4 | COMPLETED |
| 4.2 | Implement Agent Entry Point | Sub-Agent-4 | COMPLETED |
| 4.3 | Create Backend Entry and Server | Sub-Agent-4 | COMPLETED |

### Phase 5: Frontend - Core Setup and Token Integration

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 5.1 | Create LiveKit Client Configuration | Sub-Agent-2 | COMPLETED |
| 5.2 | Create Token API Route | Sub-Agent-2 | COMPLETED |
| 5.3 | Set Up App Layout | Sub-Agent-2 | COMPLETED |

### Phase 6: Frontend - Voice UI Components

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 6.1 | Create Connection Status Component | Sub-Agent-2 | COMPLETED |
| 6.2 | Create Audio Visualizer Component | Sub-Agent-2 | COMPLETED |
| 6.3 | Create Voice Agent Component | Sub-Agent-2 | COMPLETED |
| 6.4 | Create Main Voice UI Page | Sub-Agent-2 | COMPLETED |

### Phase 7: Integration and End-to-End Testing

| Task ID | Task | Assigned To | Status |
|---------|------|-------------|--------|
| 7.1 | Backend Integration Test | Master Agent | COMPLETED |
| 7.2 | Frontend-Backend Integration | Master Agent | COMPLETED |
| 7.3 | End-to-End Voice Conversation Test | Master Agent | COMPLETED |

---

## Coordination Log

| Cycle | Action | Date | Notes |
|-------|--------|------|-------|
| CYCLE-1 | Orchestration Created | 2026-01-16 | Initial distribution: SA-1 (Backend Core), SA-2 (Frontend) |
| CYCLE-1 | Sub-Agents Generated | 2026-01-16 | 4 sub-agent files created, CYCLE-1 agents READY |
| CYCLE-1 | SA-1 Completed | 2026-01-16 | Backend structure, config, token API verified |
| CYCLE-1 | SA-2 Completed | 2026-01-16 | Frontend Next.js app with all components verified |
| CYCLE-1 | Master QA Passed | 2026-01-16 | All CYCLE-1 tasks verified, no flaws found |
| CYCLE-2 | Activated | 2026-01-16 | SA-3 and SA-4 now READY for execution |
| CYCLE-2 | SA-3 Completed | 2026-01-16 | Sarvam STT/TTS wrappers implemented using livekit-plugins-sarvam |
| CYCLE-2 | SA-4 Completed | 2026-01-17 | VoicePipelineAgent implemented and verified |
| CYCLE-2 | Master QA Passed | 2026-01-17 | Final consolidation complete. All components verified. |
| COMPLETED | Feature Delivered | 2026-01-17 | Full Voice Agent stack implemented and ready. |

---

## Strategic Guidance

### For All Sub-Agents

1. **Follow Architecture:** Strictly adhere to the folder structure and file naming from `voice-agent-architecture.md`
2. **Use Pydantic Settings:** Backend config must use `pydantic-settings` for environment variable management
3. **LiveKit Best Practices:** Use official `livekit-agents` patterns for STT/TTS plugin implementation
4. **Type Safety:** Use TypeScript for frontend, Python type hints for backend
5. **Error Handling:** Implement graceful error handling for WebSocket connections (Sarvam APIs)
6. **Environment Variables:** Never hardcode API keys; always use environment configuration

### CYCLE-1 Specific

- Sub-Agent-1 and Sub-Agent-2 can work **in parallel** with zero dependencies on each other
- Backend folder structure must be created before config/api files
- Frontend Next.js initialization must complete before component creation

### CYCLE-2 Specific

- Sub-Agent-3 depends on Sub-Agent-1's completion (needs `config/settings.py`)
- Sub-Agent-4 depends on Sub-Agent-3's completion (needs plugin imports)
- Prompts file (`agent/prompts.py`) has no dependencies and can be done first

---

## Quick Reference: Invocation Commands

### CYCLE-1 Execution (Parallel)

```
# Execute Backend Core
Provide: sub-agent-1.md

# Execute Frontend Complete  
Provide: sub-agent-2.md
```

### CYCLE-1 Consolidation

```
# After both sub-agents complete
Provide: master-agent.md + sub-agent-1.md + sub-agent-2.md
```

### CYCLE-2 Execution (After Consolidation)

```
# Execute Sarvam Plugins (first)
Provide: sub-agent-3.md

# Execute Voice Agent (after plugins)
Provide: sub-agent-4.md
```

### Final Consolidation

```
# After all sub-agents complete
Provide: master-agent.md + all sub-agent-*.md files
```

---

## File Ownership Summary

| Directory/File | Owner | Cycle |
|----------------|-------|-------|
| `backend/requirements.txt` | Sub-Agent-1 | CYCLE-1 |
| `backend/.env.example` | Sub-Agent-1 | CYCLE-1 |
| `backend/config/` | Sub-Agent-1 | CYCLE-1 |
| `backend/api/` | Sub-Agent-1 | CYCLE-1 |
| `backend/plugins/` | Sub-Agent-3 | CYCLE-2 |
| `backend/agent/` | Sub-Agent-4 | CYCLE-2 |
| `frontend/` | Sub-Agent-2 | CYCLE-1 |

---

## Notes

- Phase 7 (Integration Testing) will be handled by the Master Agent during final consolidation
- All sub-agents must verify their work using linters and manual inspection before marking tasks complete
- Any blockers or cross-scope dependencies must be escalated to Master Agent immediately
