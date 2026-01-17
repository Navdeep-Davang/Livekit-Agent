"""Voice Agent Implementation using LiveKit Agents 1.0 API.

This module defines the VoiceAgent class using the modern Agent pattern.
"""
import logging
from livekit.agents import Agent, RunContext
from livekit.agents.llm import function_tool

logger = logging.getLogger("voice-agent")

SYSTEM_INSTRUCTIONS = """You are a helpful, friendly, and natural-sounding voice assistant.
Your goal is to assist the user with their queries in a conversational manner.

Guidelines:
- Keep your responses concise and suitable for voice interaction.
- Use natural language and avoid overly formal or technical jargon unless necessary.
- If you don't know the answer, politely say so.
- You can communicate in both English and Indian languages as supported by the STT/TTS plugins.
- Be proactive and helpful, but don't be overly talkative.
- Do not use emojis, asterisks, markdown, or other special characters in your responses.
"""


class VoiceAgent(Agent):
    """A voice-enabled AI assistant using Sarvam AI and OpenAI."""

    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)

    async def on_enter(self):
        """Called when the agent is added to the session.
        
        Generate an initial greeting to start the conversation.
        Keep it uninterruptible so the client has time to calibrate AEC.
        """
        self.session.generate_reply(
            instructions="Greet the user warmly and ask how you can help them today.",
            allow_interruptions=False
        )

    @function_tool
    async def get_current_time(self, context: RunContext):
        """Get the current time. Called when user asks about time."""
        from datetime import datetime
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."

    @function_tool
    async def get_current_date(self, context: RunContext):
        """Get the current date. Called when user asks about date."""
        from datetime import datetime
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
