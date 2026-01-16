'use client';

import { 
  useLocalParticipant, 
  useTracks, 
  useRoomContext,
  TrackReference
} from '@livekit/components-react';
import { Track } from 'livekit-client';
import { useState, useEffect } from 'react';
import { ConnectionStatus } from './ConnectionStatus';
import { AudioVisualizer } from './AudioVisualizer';

export function VoiceAgent() {
  const { localParticipant, isMicrophoneEnabled } = useLocalParticipant();
  const room = useRoomContext();
  
  // Get all audio tracks (local and remote)
  const tracks = useTracks([
    { source: Track.Source.Microphone, pk: localParticipant.identity },
    { source: Track.Source.Microphone, pk: 'agent' }, // Assuming agent identity is 'agent'
  ]);

  const [agentTrack, setAgentTrack] = useState<TrackReference | undefined>();
  const [userTrack, setUserTrack] = useState<TrackReference | undefined>();

  useEffect(() => {
    const agentAudio = tracks.find(t => t.participant.identity !== localParticipant.identity);
    const userAudio = tracks.find(t => t.participant.identity === localParticipant.identity);
    
    setAgentTrack(agentAudio);
    setUserTrack(userAudio);
  }, [tracks, localParticipant.identity]);

  const toggleMic = async () => {
    try {
      await localParticipant.setMicrophoneEnabled(!isMicrophoneEnabled);
    } catch (err) {
      console.error('Failed to toggle microphone:', err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-between h-full py-12 px-6">
      <div className="w-full flex justify-center mb-8">
        <ConnectionStatus />
      </div>

      <div className="flex-1 flex flex-col items-center justify-center w-full max-w-md">
        {/* Agent Visualization */}
        <div className="relative mb-12 flex flex-col items-center">
          <div className={`w-32 h-32 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center overflow-hidden transition-all duration-500 ${agentTrack?.publication?.isSubscribed ? 'animate-pulse-glow border-cyan-500/50' : ''}`}>
            {agentTrack?.publication?.isSubscribed ? (
              <div className="w-16 h-16 bg-cyan-500/20 rounded-full flex items-center justify-center animate-pulse">
                 <div className="w-8 h-8 bg-cyan-500 rounded-full" />
              </div>
            ) : (
              <div className="w-4 h-4 bg-slate-600 rounded-full" />
            )}
          </div>
          <p className="mt-4 text-slate-400 font-medium tracking-wide uppercase text-[10px]">
            AI Assistant
          </p>
          {agentTrack && <AudioVisualizer trackRef={agentTrack} barColor="#06b6d4" />}
        </div>

        {/* User Visualization & Controls */}
        <div className="w-full glass-panel p-8 flex flex-col items-center">
          <div className="mb-6 w-full h-8">
            {isMicrophoneEnabled && userTrack && (
              <AudioVisualizer trackRef={userTrack} barColor="#34d399" barCount={20} />
            )}
          </div>

          <button
            onClick={toggleMic}
            className={`group relative flex items-center justify-center w-20 h-20 rounded-full transition-all duration-300 ${
              isMicrophoneEnabled 
                ? 'bg-rose-500 hover:bg-rose-600 shadow-lg shadow-rose-500/30' 
                : 'bg-emerald-500 hover:bg-emerald-600 shadow-lg shadow-emerald-500/30'
            }`}
          >
            <div className="absolute inset-0 rounded-full animate-ping group-hover:animate-none opacity-20 bg-current" />
            
            {isMicrophoneEnabled ? (
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" strokeWidth="2" />
              </svg>
            ) : (
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>
          
          <p className="mt-4 text-sm font-medium text-slate-300">
            {isMicrophoneEnabled ? 'Mute Microphone' : 'Start Talking'}
          </p>
        </div>
      </div>

      <div className="mt-8 text-slate-500 text-xs">
        Powered by LiveKit & Sarvam AI
      </div>
    </div>
  );
}
