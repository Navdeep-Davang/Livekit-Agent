'use client';

import { ConnectionState } from 'livekit-client';
import { useConnectionState } from '@livekit/components-react';

export function ConnectionStatus() {
  const status = useConnectionState();

  const getStatusDetails = () => {
    switch (status) {
      case ConnectionState.Connected:
        return {
          label: 'Connected',
          color: 'bg-emerald-500',
          animate: false,
        };
      case ConnectionState.Connecting:
      case ConnectionState.Reconnecting:
        return {
          label: status === ConnectionState.Connecting ? 'Connecting...' : 'Reconnecting...',
          color: 'bg-amber-500',
          animate: true,
        };
      case ConnectionState.Disconnected:
        return {
          label: 'Disconnected',
          color: 'bg-rose-500',
          animate: false,
        };
      default:
        return {
          label: 'Unknown',
          color: 'bg-slate-500',
          animate: false,
        };
    }
  };

  const details = getStatusDetails();

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/50 border border-slate-700/50 backdrop-blur-sm">
      <div
        className={`w-2 h-2 rounded-full ${details.color} ${
          details.animate ? 'animate-pulse' : ''
        }`}
      />
      <span className="text-xs font-medium text-slate-300 uppercase tracking-wider">
        {details.label}
      </span>
    </div>
  );
}
