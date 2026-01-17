# Dockerfile for LiveKit Voice Agent (Backend)
FROM python:3.11-slim

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    portaudio19-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ .

# Command to run the agent worker
# Note: Ensure LIVEKIT_URL, API_KEY, and SECRET are provided via env
CMD ["python", "-m", "agent.main", "dev"]
