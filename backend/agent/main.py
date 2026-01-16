import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice_assistant import VoicePipelineAgent
from livekit.plugins import openai, silero
from plugins import SarvamSTT, SarvamTTS
from config.settings import settings
from .prompts import SYSTEM_PROMPT

logger = logging.getLogger("voice-agent")

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")
    
    # Initialize pipeline components
    # Using GPT-4o-mini as the "GPT-5 mini" placeholder
    llm = openai.LLM(model="gpt-4o-mini")
    
    # Initialize VAD
    vad = silero.VAD.load()
    
    # Initialize Sarvam plugins via their factory methods
    stt = SarvamSTT.create(language="en-IN")
    tts = SarvamTTS.create(speaker="anushka")

    # Create VoicePipelineAgent
    agent = VoicePipelineAgent(
        vad=vad,
        stt=stt,
        llm=llm,
        tts=tts,
        chat_ctx=openai.ChatContext().append(role="system", text=SYSTEM_PROMPT),
    )

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    # Start the agent pipeline
    agent.start(ctx.room)
    
    # Initial greeting
    await agent.say("Hello, how can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
