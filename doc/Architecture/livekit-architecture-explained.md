# LiveKit Voice Agent Architecture - Explained

## Why Three Services?

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR COMPUTER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐│
│   │  Docker         │    │  Token Server   │    │  Agent Worker    ││
│   │  (LiveKit SFU)  │    │  (FastAPI)      │    │  (AI Brain)      ││
│   │  Port: 7882     │    │  Port: 8000     │    │  Connects to LK  ││
│   └────────┬────────┘    └────────┬────────┘    └────────┬─────────┘│
│            │                      │                      │           │
│            │    WebRTC Media      │     JWT Token        │           │
│            └──────────────────────┼──────────────────────┘           │
│                                   │                                  │
└───────────────────────────────────┼──────────────────────────────────┘
                                    │
                              ┌─────┴─────┐
                              │  Frontend │
                              │  (Browser)│
                              └───────────┘
```

---

## What Each Service Does

### 1. LiveKit Server (Docker) - The Phone Exchange 📞

**Command:** `docker compose up`

Think of it like a **phone exchange** or **switchboard operator**:
- Routes audio/video between participants
- Doesn't understand WHAT is being said, just moves data around
- Uses WebRTC protocol (same tech as video calls in browser)
- Runs on port **7882**

**Analogy:** Like a post office - it moves packages but doesn't open them.

---

### 2. Token Server (FastAPI) - The Security Guard 🔐

**Command:** `uvicorn server:app --port 8000`

**Purpose:** Issues "tickets" (JWT tokens) to allow people into rooms.

```
Frontend: "Hey, I want to join room 'meeting-123' as 'user-bob'"
Token Server: "Here's your ticket (JWT token) - show it to LiveKit to get in"
```

**Why separate?** 
- Security: Only YOUR server can issue valid tokens
- Your frontend never sees the API secret
- You can add custom logic (e.g., check if user is logged in)

---

### 3. Agent Worker (AI Brain) - The Smart Assistant 🤖

**Command:** `python -m agent.main dev`

This is where the magic happens:

1. **Listens** to the LiveKit room for audio
2. **Silero VAD** - Detects when someone is speaking
3. **Sarvam STT** - Converts speech → text
4. **OpenAI GPT** - Thinks and generates a response
5. **Sarvam TTS** - Converts text → speech audio
6. **Sends audio** back to the room

**Analogy:** Like a Zoom participant who is an AI - they join the room, listen, and respond.

---

## The Complete Flow

```
1. USER opens frontend
   ↓
2. Frontend → Token Server: "Give me a token for room 'chat-room'"
   ↓
3. Token Server → Frontend: "Here's your JWT token"
   ↓
4. Frontend → LiveKit Docker: "I want to join with this token"
   ↓
5. LiveKit: "Welcome! You're in the room now"
   ↓
6. Agent Worker (already listening to LiveKit): "Oh, a new participant joined!"
   ↓
7. Agent: *Greets the user with a voice message*
   ↓
8. USER speaks: "What time is it?"
   ↓
9. LiveKit routes user audio → Agent Worker
   ↓
10. Agent: 
    - Silero VAD: "Speech detected!"
    - Sarvam STT: "What time is it?"
    - OpenAI: "The current time is 2:30 PM"
    - Sarvam TTS: *generates audio*
    ↓
11. Agent sends audio → LiveKit → User's browser
    ↓
12. USER hears: "The current time is 2:30 PM"
```

---

## Why Not One Big Server?

| Approach | Pros | Cons |
|----------|------|------|
| **Separate (ours)** | Can scale each independently, clear separation | 3 terminals to manage |
| **Combined** | Simpler development | Harder to scale, messier code |

In production, you might have:
- 1 Token Server handling 10,000 users
- 50 Agent Workers handling conversations
- 1 LiveKit cluster handling media

---

## Quick Reference

| Service | Command | Port | Purpose |
|---------|---------|------|---------|
| LiveKit | `docker compose up` | 7882 | Routes audio/video |
| Token Server | `uvicorn server:app --port 8000` | 8000 | Issues JWT tokens |
| Agent Worker | `python -m agent.main dev` | (connects to 7882) | AI voice assistant |

---

## Environment Variables Explained

```env
# Where is the LiveKit server?
LIVEKIT_URL=ws://localhost:7882

# Credentials to talk to LiveKit (like username/password)
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret

# API key for Sarvam (Indian STT/TTS)
SARVAM_API_KEY=your-key

# API key for OpenAI (GPT brain)
OPENAI_API_KEY=your-key
```
