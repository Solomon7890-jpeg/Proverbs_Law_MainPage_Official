"use client";

import { useState, useRef, useEffect } from "react";

const tracks = [
  { name: "528Hz Sovereign Pulse", file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", description: "Transformation & Miracles" },
  { name: "432Hz Universal Wisdom", file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", description: "Deep Introspection" },
  { name: "Deep Focus (Legal Study)", file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3", description: "Procedural Clarity" },
];

export default function AudioEngine() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrack, setCurrentTrack] = useState(0);
  const [volume, setVolume] = useState(0.5);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying(!isPlaying);
  };

  const nextTrack = () => {
    const nextIdx = (currentTrack + 1) % tracks.length;
    setCurrentTrack(nextIdx);
    if (isPlaying && audioRef.current) {
      audioRef.current.src = tracks[nextIdx].file;
      audioRef.current.play();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 group">
      <div className="flex items-center gap-4 rounded-full border border-zinc-800 bg-zinc-950/40 p-2 backdrop-blur-xl shadow-2xl transition-all hover:pr-6">
        {/* Visualizer-ish Pulse */}
        <div className={`h-10 w-10 flex items-center justify-center rounded-full bg-zinc-900 border border-zinc-800 cursor-pointer overflow-hidden relative ${isPlaying ? 'animate-pulse shadow-[0_0_20px_rgba(156,142,125,0.3)]' : ''}`} onClick={togglePlay}>
          <span className="text-xl">{isPlaying ? "⏸️" : "▶️"}</span>
        </div>

        {/* Track Info (Hidden until hover) */}
        <div className="flex flex-col opacity-0 group-hover:opacity-100 transition-opacity duration-300 max-w-0 group-hover:max-w-xs overflow-hidden">
          <span className="text-xs font-bold text-[#9C8E7D] whitespace-nowrap">{tracks[currentTrack].name}</span>
          <span className="text-[10px] text-zinc-500 whitespace-nowrap">{tracks[currentTrack].description}</span>
        </div>

        {/* Controls (Hidden until hover) */}
        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <button onClick={nextTrack} className="text-zinc-400 hover:text-white transition">⏭️</button>
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.01" 
            value={volume} 
            onChange={(e) => setVolume(parseFloat(e.target.value))}
            className="w-16 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-[#9C8E7D]"
            aria-label="Volume Control"
            title="Volume Control"
          />
        </div>
      </div>

      <audio 
        ref={audioRef} 
        src={tracks[currentTrack].file} 
        onEnded={() => nextTrack()}
        crossOrigin="anonymous"
      />
    </div>
  );
}
