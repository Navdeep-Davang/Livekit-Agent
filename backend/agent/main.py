import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, silero, cartesia, sarvam

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")

SYSTEM_INSTRUCTIONS = """You are a helpful, friendly, and natural-sounding voice assistant.
Your goal is to assist the user with their queries in a conversational manner.

Guidelines:
- Keep your responses concise and natural.
- Use natural language and avoid technical jargon.
- Do not use markdown, emojis, or special characters.
"""

class Assistant(Agent):
    """Voice Assistant using OpenAI, Cartesia, and Sarvam."""
    def __init__(self):
        super().__init__(instructions=SYSTEM_INSTRUCTIONS)

    @function_tool
    async def get_current_date_and_time(self, context: RunContext) -> str:
        """Get the current date and time. Use this when the user asks for the time or date."""
        current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        return f"The current date and time is {current_datetime}"

async def entrypoint(ctx: JobContext):
    """Entry point for the LiveKit agent."""
    logger.info(f"Connecting to room: {ctx.room.name}")
    
    # Connect to the room
    await ctx.connect()

    # Configure the voice pipeline with reliable providers
    session = AgentSession(
        stt=cartesia.STT(model="ink-whisper"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=sarvam.TTS(target_language_code="en-IN", speaker="anushka"),
        vad=silero.VAD.load(),
    )

    # Start the session with the assistant
    await session.start(
        room=ctx.room,
        agent=Assistant()
    )

    # Generate initial greeting
    await session.generate_reply(
        instructions="Greet the user warmly and ask how you can help."
    )

if __name__ == "__main__":
    # Run the agent in the standard LiveKit pattern
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
