from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from livekit import api
from config import settings
import os

router = APIRouter()

class TokenRequest(BaseModel):
    room: str
    identity: str

class TokenResponse(BaseModel):
    token: str

@router.post("/token", response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    try:
        # Create AccessToken
        token = api.AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET
        )
        
        # Set identity and grants
        token.with_identity(request.identity)
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=request.room,
            room_admin=True
        ))
        
        return TokenResponse(token=token.to_jwt())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
