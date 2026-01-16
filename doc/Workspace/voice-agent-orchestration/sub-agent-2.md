# Sub-Agent-2: Frontend Complete

---

## Your Assignment

| Property | Value |
|----------|-------|
| **Orchestration** | Voice Agent End-to-End Implementation |
| **Cycle** | CYCLE-1 |
| **Role** | Frontend - Next.js Voice UI |

---

## Strategic Context & Prompts

You are responsible for building the **complete frontend** of the Voice Agent system. This is a Next.js application that connects to LiveKit for real-time audio streaming and provides a beautiful, modern voice interaction UI.

### Key Objectives

1. **Next.js Setup:** Initialize a TypeScript Next.js app with proper configuration
2. **LiveKit Integration:** Configure the LiveKit client library for WebRTC audio
3. **Token Flow:** Create an API route that fetches tokens from the backend
4. **Voice UI:** Build intuitive, visually appealing components for voice interaction

### Technical Guidance

- Use Next.js App Router (app/ directory)
- Use `@livekit/components-react` for LiveKit React integration
- Use `livekit-client` for lower-level control when needed
- Implement a beautiful, modern UI with:
  - Smooth animations for connection states
  - Visual audio feedback (waveform/visualizer)
  - Clear microphone on/off states
- Use CSS modules or Tailwind for styling
- Handle connection errors gracefully with user feedback

### UI/UX Requirements

- **Color Scheme:** Use a dark theme with accent colors for active states
- **Animations:** Smooth transitions for connection states, pulsing for active speaking
- **Audio Visualizer:** Show real-time audio levels/waveform when speaking
- **Responsive:** Works well on desktop and mobile

---

## Scope & Constraints

### What You Own

```
frontend/
├── package.json              # YOU CREATE THIS
├── tsconfig.json             # YOU CREATE THIS (via Next.js init)
├── next.config.js            # YOU CREATE THIS (via Next.js init)
├── .env.local.example        # YOU CREATE THIS
├── tailwind.config.js        # YOU CREATE THIS (if using Tailwind)
├── app/
│   ├── layout.tsx            # YOU CREATE THIS
│   ├── page.tsx              # YOU CREATE THIS
│   ├── globals.css           # YOU CREATE THIS
│   └── api/
│       └── token/
│           └── route.ts      # YOU CREATE THIS
├── components/
│   ├── VoiceAgent.tsx        # YOU CREATE THIS
│   ├── AudioVisualizer.tsx   # YOU CREATE THIS
│   └── ConnectionStatus.tsx  # YOU CREATE THIS
└── lib/
    └── livekit.ts            # YOU CREATE THIS
```

### What You DON'T Touch

- `backend/` - Owned by Sub-Agent-1, 3, 4
- Any files outside `frontend/`

---

## Your Tasks

### Phase 1.2: Initialize Frontend Next.js Project

- [ ] **Subtask 1.2.1:** Create Next.js app in `frontend/` with TypeScript
  - Use `create-next-app` or manual setup
  - Configure for App Router
  - Set up Tailwind CSS for styling

- [ ] **Subtask 1.2.2:** Install dependencies
  - `@livekit/components-react`
  - `livekit-client`
  - Any additional UI dependencies

- [ ] **Subtask 1.2.3:** Create `frontend/.env.local.example`
  ```
  NEXT_PUBLIC_LIVEKIT_URL=wss://your-app.livekit.cloud
  NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
  ```

### Phase 5.1: Create LiveKit Client Configuration

- [ ] **Subtask 5.1.1:** Implement `frontend/lib/livekit.ts`
  - Export LiveKit client configuration
  - Helper functions for room connection
  - Audio track configuration defaults

### Phase 5.2: Create Token API Route

- [ ] **Subtask 5.2.1:** Implement `frontend/app/api/token/route.ts`
  - Create POST handler
  - Accept `room` and `identity` from request body
  - Proxy request to backend token endpoint
  - Return token to client

### Phase 5.3: Set Up App Layout

- [ ] **Subtask 5.3.1:** Configure `frontend/app/layout.tsx`
  - Set proper metadata (title, description)
  - Import global styles
  - Set up font (use a modern, clean font)

- [ ] **Subtask 5.3.2:** Create `frontend/app/globals.css`
  - Define CSS variables for theme colors
  - Set up dark theme base styles
  - Include Tailwind directives

### Phase 6.1: Create Connection Status Component

- [ ] **Subtask 6.1.1:** Implement `frontend/components/ConnectionStatus.tsx`
  - Show current connection state (disconnected, connecting, connected)
  - Use distinct colors/icons for each state
  - Animate state transitions

### Phase 6.2: Create Audio Visualizer Component

- [ ] **Subtask 6.2.1:** Implement `frontend/components/AudioVisualizer.tsx`
  - Display audio levels or waveform
  - React to audio track data
  - Smooth, visually appealing animation
  - Support for both input (user) and output (agent) audio

### Phase 6.3: Create Voice Agent Component

- [ ] **Subtask 6.3.1:** Implement `frontend/components/VoiceAgent.tsx`
  - Main voice interaction component
  - Microphone toggle button (on/off)
  - Use LiveKit hooks for room/track management
  - Handle audio track publishing/subscribing
  - Integrate ConnectionStatus and AudioVisualizer

### Phase 6.4: Create Main Voice UI Page

- [ ] **Subtask 6.4.1:** Implement `frontend/app/page.tsx`
  - Main voice UI page
  - Token fetching logic (call /api/token)
  - LiveKit room provider setup
  - Render VoiceAgent component
  - Handle errors and loading states

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
| 1.2.1 | [X] | Terminal output & directory listing | Next.js 14 initialized in frontend/ |
| 1.2.2 | [X] | package.json check | LiveKit dependencies installed |
| 1.2.3 | [X] | Terminal (echo/Set-Content) | .env.local.example created |
| 5.1.1 | [X] | File inspection | lib/livekit.ts implemented |
| 5.2.1 | [X] | File inspection | app/api/token/route.ts implemented |
| 5.3.1 | [X] | File inspection | app/layout.tsx configured |
| 5.3.2 | [X] | File inspection | app/globals.css configured |
| 6.1.1 | [X] | File inspection | ConnectionStatus.tsx implemented |
| 6.2.1 | [X] | File inspection | AudioVisualizer.tsx implemented |
| 6.3.1 | [X] | File inspection | VoiceAgent.tsx implemented |
| 6.4.1 | [X] | File inspection | app/page.tsx implemented |

---

## Implementation Checklist

- [X] Logic implemented as per Strategic Context
- [X] Code follows project conventions
- [X] No new linter errors introduced
- [X] Verification performed (describe method in notes)
- [X] Ready for Master QA

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
