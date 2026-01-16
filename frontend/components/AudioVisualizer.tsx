'use client';

import { useEffect, useRef } from 'react';
import { TrackReference } from '@livekit/components-react';
import { LocalAudioTrack, RemoteAudioTrack } from 'livekit-client';

interface AudioVisualizerProps {
  trackRef?: TrackReference;
  barColor?: string;
  barCount?: number;
}

export function AudioVisualizer({
  trackRef,
  barColor = '#06b6d4',
  barCount = 15,
}: AudioVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);
  const analyserRef = useRef<AnalyserNode | null>(null);

  useEffect(() => {
    if (!trackRef?.publication?.track) return;
    
    const track = trackRef.publication.track as LocalAudioTrack | RemoteAudioTrack;
    const mediaStream = new MediaStream([track.mediaStreamTrack]);
    
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(mediaStream);
    
    source.connect(analyser);
    analyser.fftSize = 64;
    analyserRef.current = analyser;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      if (!canvasRef.current) return;
      
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const width = canvas.width;
      const height = canvas.height;

      analyser.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, width, height);

      const barWidth = (width / barCount) * 0.8;
      const barSpacing = (width / barCount) * 0.2;
      
      for (let i = 0; i < barCount; i++) {
        // Average the frequency data for each bar
        const dataIndex = Math.floor((i / barCount) * bufferLength);
        const value = dataArray[dataIndex];
        const barHeight = (value / 255) * height;

        const x = i * (barWidth + barSpacing);
        const y = height - barHeight;

        // Draw rounded bars
        ctx.fillStyle = barColor;
        
        // Add glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = barColor;
        
        // Draw centered bars
        const centerY = height / 2;
        const h = Math.max(4, barHeight);
        ctx.beginPath();
        ctx.roundRect(x, centerY - h / 2, barWidth, h, barWidth / 2);
        ctx.fill();
      }

      animationRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationRef.current);
      audioContext.close();
    };
  }, [trackRef, barColor, barCount]);

  return (
    <div className="w-full h-12 flex items-center justify-center">
      <canvas
        ref={canvasRef}
        width={300}
        height={48}
        className="w-full max-w-[200px] h-full"
      />
    </div>
  );
}
