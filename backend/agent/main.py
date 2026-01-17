"""LiveKit Voice Agent Entry Point.

This module sets up the AgentServer and entrypoint using the modern 1.0 API pattern.
Run with: python -m agent.main dev
"""
import logging
import os
from dotenv import load_dotenv

from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    metrics,
    MetricsCollectedEvent,
)
from livekit.plugins import openai, sarvam, silero

from .voice_agent import VoiceAgent

# Load environment variables from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv()  # Also check current directory

# Set up logging - enable DEBUG for Sarvam to see raw messages
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

# Enable DEBUG level for Sarvam plugin to see all WebSocket messages
logging.getLogger("livekit.plugins.sarvam").setLevel(logging.DEBUG)
logging.getLogger("livekit.plugins.sarvam.log").setLevel(logging.DEBUG)
logging.getLogger("livekit.plugins.sarvam.log.SpeechStream").setLevel(logging.DEBUG)

# Create the AgentServer
server = AgentServer()


def prewarm(proc: JobProcess):
    """Prewarm function to load VAD model before session starts.
    
    This runs once per worker process, not per session.
    """
    logger.info("Prewarming: Loading Silero VAD model...")
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("Prewarming complete: VAD model loaded")


# Set the prewarm function
server.setup_fnc = prewarm


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    """Entry point for each RTC session.
    
    This is called when a new participant joins a room that needs an agent.
    """
    # Add room name to log context
    ctx.log_context_fields = {"room": ctx.room.name}
    
    logger.info(f"Starting agent session for room: {ctx.room.name}")
    
    # Connect the agent to the room - CRITICAL: without this, agent never joins!
    await ctx.connect()
    
    # Get API key from environment
    sarvam_api_key = os.environ.get("SARVAM_API_KEY")
    if not sarvam_api_key:
        logger.error("SARVAM_API_KEY not found in environment")
        raise ValueError("SARVAM_API_KEY environment variable is required")
    
    # Configure the AgentSession with all pipeline components
    session = AgentSession(
        # Speech-to-text using Sarvam AI
        stt=sarvam.STT(
            language="en-IN",
            model="saarika:v2.5",
            api_key=sarvam_api_key,
            flush_signal=True,  # CRITICAL: enables transcript delivery after VAD END_SPEECH
        ),
        # LLM using OpenAI
        llm=openai.LLM(model="gpt-4o-mini"),
        # Text-to-speech using Sarvam AI
        tts=sarvam.TTS(
            target_language_code="en-IN",
            speaker="anushka",
            model="bulbul:v2",
            api_key=sarvam_api_key,
        ),
        # Voice Activity Detection (preloaded in prewarm)
        vad=ctx.proc.userdata["vad"],
        # Turn detection using VAD (more reliable for debugging)
        turn_detection="vad",
        # Enable preemptive generation for faster responses
        preemptive_generation=True,
        # Resume speech on false interruptions (background noise)
        resume_false_interruption=True,
        false_interruption_timeout=1.0,
    )
    
    # Set up metrics collection
    usage_collector = metrics.UsageCollector()
    
    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)
    
    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Session usage: {summary}")
    
    # Register shutdown callback
    ctx.add_shutdown_callback(log_usage)
    
    # Start the agent session
    await session.start(
        agent=VoiceAgent(),
        room=ctx.room,
    )
    
    logger.info(f"Agent session started for room: {ctx.room.name}")


if __name__ == "__main__":
    cli.run_app(server)
