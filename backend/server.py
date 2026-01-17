"""FastAPI Token Server for LiveKit.

This server provides JWT token generation for LiveKit room access.
Run separately from the agent worker.

Usage: uvicorn server:app --port 8000
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("token-server")

app = FastAPI(
    title="LiveKit Token Server",
    description="JWT token generation for LiveKit room access",
    version="1.0.0"
)

# Add CORS middleware to allow the frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "LiveKit Token Server is running",
        "endpoints": {
            "token": "/api/token",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
