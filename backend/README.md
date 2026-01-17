# LiveKit Voice Agent - Backend

This is the FastAPI token server and LiveKit agent worker for the voice assistant.

## Getting Started

### Prerequisites
- Python 3.11+
- [LiveKit Cloud](https://cloud.livekit.io) account or local LiveKit server

### Environment Setup
Ensure you have a `.env` file in the **project root** (`Livekit-Agent/.env`) with:

```env
LIVEKIT_URL=wss://your-app.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
SARVAM_API_KEY=your-sarvam-key
OPENAI_API_KEY=your-openai-key
```

### Installation

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Backend

The backend runs as **two separate processes**:

#### Terminal 1: Token Server (FastAPI)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn server:app --port 8000
```

#### Terminal 2: Agent Worker (LiveKit)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m agent.main dev
```

### Testing Locally

For quick local testing without a LiveKit server:
```powershell
python -m agent.main console
```

This runs the agent in console mode where you can interact via terminal audio.

### Production

```powershell
python -m agent.main start
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server status |
| `/health` | GET | Health check |
| `/api/token` | POST | Generate LiveKit JWT token |

### Token Request

```json
POST /api/token
{
  "room": "my-room",
  "identity": "user-123"
}
```

### Token Response

```json
{
  "token": "eyJhbGci..."
}
```

## Architecture

```
User speaks → Frontend (WebRTC) → LiveKit Room → Agent Worker
    ↓
Silero VAD detects speech
    ↓
Sarvam STT → Text
    ↓
OpenAI GPT-4o-mini → Response text
    ↓
Sarvam TTS → Audio
    ↓
LiveKit Room → Frontend (WebRTC) → User hears response
```

## Project Structure

```
backend/
├── agent/
│   ├── __init__.py
│   ├── main.py          # AgentServer + entrypoint
│   └── voice_agent.py   # Agent class with instructions
├── api/
│   ├── __init__.py
│   └── token.py         # Token generation endpoint
├── config/
│   ├── __init__.py
│   └── settings.py      # Pydantic settings
├── plugins/             # (Empty - using official plugins)
├── requirements.txt
└── server.py            # FastAPI token server
```
