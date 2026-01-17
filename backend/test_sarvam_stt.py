"""
Standalone Sarvam STT Test Script

This script tests Sarvam STT streaming independently from LiveKit
to verify the API works correctly.

Usage:
    python test_sarvam_stt.py

Make sure to have a .env file with SARVAM_API_KEY set.
"""

import asyncio
import os
import base64
import json
import wave
import struct
import aiohttp
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv()

SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY")
SARVAM_STT_WS_URL = "wss://api.sarvam.ai/speech-to-text/ws"


def generate_test_audio(duration_seconds: float = 3.0, sample_rate: int = 16000) -> bytes:
    """Generate a simple sine wave test audio."""
    import math
    
    frequency = 440  # A4 note
    num_samples = int(sample_rate * duration_seconds)
    amplitude = 16000  # Int16 max is 32767
    
    samples = []
    for i in range(num_samples):
        # Generate sine wave
        value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        samples.append(struct.pack('<h', value))
    
    return b''.join(samples)


async def test_sarvam_stt_streaming():
    """Test Sarvam STT streaming API directly."""
    
    if not SARVAM_API_KEY:
        print("❌ SARVAM_API_KEY not found in environment")
        return False
    
    print(f"✅ SARVAM_API_KEY found (length: {len(SARVAM_API_KEY)})")
    
    # Build WebSocket URL
    params = {
        "language-code": "en-IN",
        "model": "saarika:v2.5",
        "vad_signals": "true",
        "sample_rate": "16000",
    }
    ws_url = f"{SARVAM_STT_WS_URL}?{urlencode(params)}"
    
    print(f"\n📡 Connecting to: {ws_url}")
    
    # Headers for authentication
    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(ws_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as ws:
                print("✅ WebSocket connected successfully!")
                
                # Generate test audio (silence/tone)
                print("\n🎤 Generating test audio (3 seconds of tone)...")
                audio_data = generate_test_audio(3.0, 16000)
                
                # Send audio in chunks
                chunk_size = 800  # 50ms at 16kHz
                num_chunks = len(audio_data) // (chunk_size * 2)  # *2 for Int16
                print(f"📤 Sending {num_chunks} audio chunks...")
                
                # Create a task to receive messages
                async def receive_messages():
                    received_count = 0
                    try:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                received_count += 1
                                msg_type = data.get("type", "unknown")
                                print(f"\n📥 Received message #{received_count}: type={msg_type}")
                                print(f"   Data: {json.dumps(data, indent=2)[:500]}...")
                                
                                if msg_type == "data":
                                    transcript = data.get("data", {}).get("transcript", "")
                                    if transcript:
                                        print(f"\n🎉 TRANSCRIPT: {transcript}")
                                elif msg_type == "events":
                                    signal = data.get("data", {}).get("signal_type", "")
                                    print(f"   VAD Event: {signal}")
                                elif msg_type == "error":
                                    print(f"   ❌ Error: {data}")
                                    
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                print(f"❌ WebSocket error: {ws.exception()}")
                                break
                            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSE):
                                print("🔌 WebSocket closed")
                                break
                    except Exception as e:
                        print(f"❌ Error receiving: {e}")
                    
                    print(f"\n📊 Total messages received: {received_count}")
                
                # Start receiving in background
                receive_task = asyncio.create_task(receive_messages())
                
                # Send audio chunks
                for i in range(num_chunks):
                    start = i * chunk_size * 2
                    end = start + chunk_size * 2
                    chunk = audio_data[start:end]
                    
                    # Convert to base64
                    b64_chunk = base64.b64encode(chunk).decode('utf-8')
                    
                    # Build message
                    audio_message = {
                        "audio": {
                            "data": b64_chunk,
                            "encoding": "audio/wav",
                            "sample_rate": 16000,
                        }
                    }
                    
                    await ws.send_str(json.dumps(audio_message))
                    
                    if (i + 1) % 20 == 0:
                        print(f"   Sent {i + 1}/{num_chunks} chunks...")
                    
                    await asyncio.sleep(0.05)  # 50ms between chunks (real-time)
                
                print(f"\n✅ Sent all {num_chunks} audio chunks")
                
                # Send end of stream
                eos_message = {
                    "type": "end_of_stream",
                    "audio": {
                        "data": "",
                        "encoding": "audio/wav",
                        "sample_rate": 16000,
                    }
                }
                await ws.send_str(json.dumps(eos_message))
                print("📤 Sent end_of_stream signal")
                
                # Wait a bit for responses
                print("\n⏳ Waiting for responses (5 seconds)...")
                await asyncio.sleep(5)
                
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass
                
                print("\n✅ Test completed!")
                return True
                
        except aiohttp.ClientError as e:
            print(f"❌ Connection error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {e}")
            return False


async def test_sarvam_stt_rest():
    """Test Sarvam STT REST API (non-streaming) as a baseline."""
    
    if not SARVAM_API_KEY:
        print("❌ SARVAM_API_KEY not found")
        return False
    
    print("\n📡 Testing REST API (non-streaming)...")
    
    # Generate a short test audio file
    audio_data = generate_test_audio(1.0, 16000)
    
    # Create a WAV file in memory
    import io
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(audio_data)
    
    wav_bytes = wav_buffer.getvalue()
    
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }
    
    form_data = aiohttp.FormData()
    form_data.add_field('file', wav_bytes, filename='test.wav', content_type='audio/wav')
    form_data.add_field('language_code', 'en-IN')
    form_data.add_field('model', 'saarika:v2.5')
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=form_data, headers=headers) as resp:
                print(f"   Status: {resp.status}")
                response_text = await resp.text()
                print(f"   Response: {response_text[:500]}")
                
                if resp.status == 200:
                    print("✅ REST API works!")
                    return True
                else:
                    print(f"❌ REST API error: {resp.status}")
                    return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


async def main():
    print("=" * 60)
    print("SARVAM STT API TEST")
    print("=" * 60)
    
    # Test 1: REST API with real audio file
    print("\n" + "=" * 40)
    print("TEST 1: REST API with assistant.wav")
    print("=" * 40)
    rest_ok = await test_sarvam_stt_rest_with_file()
    
    # Test 2: Streaming API with real audio file
    print("\n" + "=" * 40)
    print("TEST 2: WebSocket Streaming with assistant.wav")
    print("=" * 40)
    streaming_ok = await test_sarvam_stt_streaming_with_file()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"REST API:      {'✅ PASS' if rest_ok else '❌ FAIL'}")
    print(f"Streaming API: {'✅ PASS' if streaming_ok else '❌ FAIL'}")


async def test_sarvam_stt_rest_with_file():
    """Test Sarvam STT REST API with assistant.wav file."""
    
    if not SARVAM_API_KEY:
        print("❌ SARVAM_API_KEY not found")
        return False
    
    audio_file = os.path.join(os.path.dirname(__file__), "assistant.wav")
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    print(f"📁 Using audio file: {audio_file}")
    
    with open(audio_file, 'rb') as f:
        wav_bytes = f.read()
    
    print(f"   File size: {len(wav_bytes)} bytes")
    
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }
    
    form_data = aiohttp.FormData()
    form_data.add_field('file', wav_bytes, filename='assistant.wav', content_type='audio/wav')
    form_data.add_field('language_code', 'en-IN')
    form_data.add_field('model', 'saarika:v2.5')
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=form_data, headers=headers) as resp:
                print(f"   Status: {resp.status}")
                response_json = await resp.json()
                print(f"   Response: {json.dumps(response_json, indent=2)}")
                
                transcript = response_json.get("transcript", "")
                if transcript:
                    print(f"\n🎉 TRANSCRIPT: {transcript}")
                    return True
                else:
                    print("⚠️  Empty transcript returned")
                    return resp.status == 200
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


async def test_sarvam_stt_streaming_with_file():
    """Test Sarvam STT streaming with assistant.wav file."""
    
    if not SARVAM_API_KEY:
        print("❌ SARVAM_API_KEY not found")
        return False
    
    audio_file = os.path.join(os.path.dirname(__file__), "assistant.wav")
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Read WAV file
    with wave.open(audio_file, 'rb') as wav:
        sample_rate = wav.getframerate()
        num_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        num_frames = wav.getnframes()
        
        # Limit to first 10 seconds for faster testing
        max_frames = sample_rate * 10  # 10 seconds
        frames_to_read = min(num_frames, max_frames)
        audio_data = wav.readframes(frames_to_read)
        duration = frames_to_read / sample_rate
        
        print(f"📁 Audio file info:")
        print(f"   Sample rate: {sample_rate} Hz")
        print(f"   Channels: {num_channels}")
        print(f"   Sample width: {sample_width} bytes")
        print(f"   Using first {duration:.2f} seconds of audio")
    
    # Build WebSocket URL - include flush_signal=true to get transcripts
    params = {
        "language-code": "en-IN",
        "model": "saarika:v2.5",
        "vad_signals": "true",
        "sample_rate": str(sample_rate),
        "flush_signal": "true",  # Enable flush signal for transcripts
    }
    ws_url = f"{SARVAM_STT_WS_URL}?{urlencode(params)}"
    
    print(f"\n📡 Connecting to: {ws_url}")
    
    headers = {"api-subscription-key": SARVAM_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(ws_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as ws:
                print("✅ WebSocket connected!")
                
                # Send audio in chunks (50ms each)
                bytes_per_sample = sample_width * num_channels
                chunk_samples = int(sample_rate * 0.05)  # 50ms
                chunk_size = chunk_samples * bytes_per_sample
                num_chunks = len(audio_data) // chunk_size
                
                print(f"📤 Sending {num_chunks} audio chunks ({chunk_size} bytes each)...")
                
                transcripts = []
                
                # Receiver task
                async def receive_messages():
                    try:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                msg_type = data.get("type", "unknown")
                                print(f"📥 {msg_type}: ", end="")
                                
                                if msg_type == "data":
                                    transcript = data.get("data", {}).get("transcript", "")
                                    if transcript:
                                        transcripts.append(transcript)
                                        print(f"'{transcript}'")
                                    else:
                                        print("(empty)")
                                elif msg_type == "events":
                                    signal = data.get("data", {}).get("signal_type", "")
                                    print(f"{signal}")
                                elif msg_type == "error":
                                    print(f"ERROR: {data}")
                                else:
                                    print(f"{data}")
                            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSE):
                                break
                    except Exception as e:
                        print(f"Receive error: {e}")
                
                receive_task = asyncio.create_task(receive_messages())
                
                # Send chunks
                for i in range(num_chunks):
                    start = i * chunk_size
                    end = start + chunk_size
                    chunk = audio_data[start:end]
                    
                    b64_chunk = base64.b64encode(chunk).decode('utf-8')
                    
                    audio_message = {
                        "audio": {
                            "data": b64_chunk,
                            "encoding": "audio/wav",
                            "sample_rate": sample_rate,
                        }
                    }
                    
                    await ws.send_str(json.dumps(audio_message))
                    
                    if (i + 1) % 20 == 0:
                        print(f"   Sent {i + 1}/{num_chunks}...")
                    
                    await asyncio.sleep(0.05)
                
                print(f"\n✅ Sent all chunks")
                
                # Send flush signal to trigger transcript
                flush_msg = {"type": "flush"}
                await ws.send_str(json.dumps(flush_msg))
                print("📤 Sent flush signal")
                
                # Wait for transcript after flush
                await asyncio.sleep(2)
                
                # End of stream
                eos = {"type": "end_of_stream", "audio": {"data": "", "encoding": "audio/wav", "sample_rate": sample_rate}}
                await ws.send_str(json.dumps(eos))
                print("📤 Sent end_of_stream")
                
                # Wait longer for responses (5 seconds)
                print("\n⏳ Waiting for transcript (5 seconds)...")
                await asyncio.sleep(5)
                receive_task.cancel()
                
                if transcripts:
                    print(f"\n🎉 FULL TRANSCRIPT: {' '.join(transcripts)}")
                    return True
                else:
                    print("\n⚠️  No transcripts received")
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


if __name__ == "__main__":
    asyncio.run(main())
