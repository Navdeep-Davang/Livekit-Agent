import { RoomOptions, VideoPresets, Track } from 'livekit-client';

export const roomOptions: RoomOptions = {
  // Automatically subscribe to tracks
  adaptiveStream: true,
  dynacast: true,
  // Audio-focused settings
  publishDefaults: {
    audioPreset: {
      maxBitrate: 48000,
    },
    dtx: true,
    red: true,
  },
  videoCaptureDefaults: {
    resolution: VideoPresets.h720.resolution,
  },
};

export const defaultAudioTrackOptions = {
  echoCancellation: true,
  noiseSuppression: true,
  autoGainControl: true,
};
