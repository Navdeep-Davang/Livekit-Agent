'use client';

import { 
  LiveKitRoom,
  RoomAudioRenderer,
} from '@livekit/components-react';
import { useState, useCallback } from 'react';
import { VoiceAgent } from '@/components/VoiceAgent';
import { roomOptions } from '@/lib/livekit';

export default function Home() {
  const [token, setToken] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startSession = useCallback(async () => {
    setIsConnecting(true);
    setError(null);
    
    try {
      const roomName = 'voice-agent-room';
      const identity = `user-${Math.floor(Math.random() * 10000)}`;
      
      const response = await fetch('/api/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ room: roomName, identity }),
      });

      if (!response.ok) {
        throw new Error('Could not fetch connection token');
      }

      const { token } = await response.json();
      setToken(token);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsConnecting(false);
    }
  }, []);

  const serverUrl = process.env.NEXT_PUBLIC_LIVEKIT_URL;

  if (!token) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen bg-slate-950 px-6">
        <div className="max-w-md w-full text-center">
          <div className="mb-8 flex justify-center">
            <div className="w-20 h-20 rounded-2xl bg-cyan-500/10 flex items-center justify-center border border-cyan-500/20">
              <svg className="w-10 h-10 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">
            AI Voice Assistant
          </h1>
          <p className="text-slate-400 mb-12 text-lg">
            Experience real-time conversations with our AI agent.
          </p>

          <button
            onClick={startSession}
            disabled={isConnecting}
            className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-300 ${
              isConnecting 
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                : 'bg-cyan-600 hover:bg-cyan-500 text-white shadow-xl shadow-cyan-900/20 hover:scale-[1.02]'
            }`}
          >
            {isConnecting ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Preparing Session...
              </span>
            ) : (
              'Start Conversation'
            )}
          </button>

          {error && (
            <div className="mt-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
              {error}
            </div>
          )}
          
          <div className="mt-12 flex items-center justify-center gap-8 opacity-50">
            <span className="text-[10px] text-slate-500 uppercase tracking-[0.2em]">Next.js 14</span>
            <span className="text-[10px] text-slate-500 uppercase tracking-[0.2em]">LiveKit</span>
            <span className="text-[10px] text-slate-500 uppercase tracking-[0.2em]">Sarvam AI</span>
          </div>
        </div>
      </main>
    );
  }

  return (
    <LiveKitRoom
      serverUrl={serverUrl}
      token={token}
      connect={true}
      options={roomOptions}
      onDisconnected={() => {
        setToken(null);
        setError('Disconnected from room');
      }}
      className="h-screen bg-slate-950"
    >
      <VoiceAgent />
      <RoomAudioRenderer />
    </LiveKitRoom>
  );
}
