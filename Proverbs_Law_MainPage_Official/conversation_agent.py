"""
Conversation Agent with Audio Support
Handles Q&A interactions with text-to-speech capabilities
"""

import asyncio
import io
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import tempfile

try:
    import edge_tts
except ImportError:
    edge_tts = None

import numpy as np
import soundfile as sf


class ConversationAgent:
    """
    Conversation agent for handling Q&A with audio support
    Features:
    - Multi-turn conversation tracking
    - Text-to-speech (TTS) for responses
    - Conversation history management
    - Audio file generation
    """

    def __init__(self, voice: str = "en-US-AriaNeural", rate: float = 1.0, pitch: int = 0):
        """
        Initialize conversation agent

        Args:
            voice: Edge TTS voice (default: Aria, US English)
            rate: Speech rate (0.5-2.0, default 1.0)
            pitch: Pitch adjustment (-20 to 20, default 0)
        """
        self.voice = voice
        self.rate = rate
        self.pitch = pitch
        self.conversation_history: List[Dict] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.tts_available = edge_tts is not None

        # Available voices (popular options)
        self.available_voices = {
            "aria_us": "en-US-AriaNeural",
            "guy_us": "en-US-GuyNeural",
            "amber_us": "en-US-AmberNeural",
            "ana_es": "es-ES-ElviraNeural",
            "pierre_fr": "fr-FR-HenriNeural",
        }

    def add_turn(self, user_query: str, assistant_response: str, mode: str = "general", ai_provider: str = "huggingface"):
        """Add a conversation turn to history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_query,
            "assistant": assistant_response,
            "mode": mode,
            "ai_provider": ai_provider
        })

    def get_conversation_context(self, max_turns: int = 5) -> str:
        """Get formatted conversation context for follow-up questions"""
        if not self.conversation_history:
            return ""

        recent_turns = self.conversation_history[-max_turns:]
        context = "Previous conversation context:\n"

        for i, turn in enumerate(recent_turns, 1):
            context += f"\n[Turn {i}]\nQ: {turn['user']}\nA: {turn['assistant'][:200]}...\n"

        return context

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_history_summary(self) -> Dict:
        """Get summary statistics of conversation"""
        return {
            "total_turns": len(self.conversation_history),
            "session_id": self.session_id,
            "first_turn": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "last_turn": self.conversation_history[-1]["timestamp"] if self.conversation_history else None,
            "ai_providers_used": list(set(turn["ai_provider"] for turn in self.conversation_history)),
            "modes_used": list(set(turn["mode"] for turn in self.conversation_history))
        }

    async def text_to_speech(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice: Optional[str] = None
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Convert text to speech using Edge TTS

        Args:
            text: Text to convert
            output_path: Optional path to save audio file
            voice: Optional voice override

        Returns:
            Tuple of (audio_bytes, output_file_path)
        """
        if not self.tts_available:
            return None, None

        if not text or len(text.strip()) == 0:
            return None, None

        try:
            voice_name = voice or self.voice

            # Sanitize text to max 2000 characters (Edge TTS limit per request)
            text = text[:2000]

            # Create temporary file if no output path specified
            if output_path is None:
                output_path = os.path.join(tempfile.gettempdir(), f"proverbs_tts_{self.session_id}.mp3")

            # Format voice string for edge-tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_name,
                rate=f"{self.rate:+.0%}".replace("+", "+") if self.rate != 1.0 else "+0%",
                pitch=f"{self.pitch:+d}Hz" if self.pitch != 0 else "+0Hz"
            )

            # Save to file
            await communicate.save(output_path)

            # Read file as bytes
            with open(output_path, 'rb') as f:
                audio_bytes = f.read()

            return audio_bytes, output_path

        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return None, None

    async def process_response_with_audio(
        self,
        text: str,
        enable_audio: bool = True,
        voice: Optional[str] = None
    ) -> Dict:
        """
        Process response and optionally generate audio

        Args:
            text: Response text
            enable_audio: Whether to generate audio
            voice: Optional voice override

        Returns:
            Dictionary with text and audio data
        """
        result = {
            "text": text,
            "audio": None,
            "audio_path": None,
            "audio_available": False
        }

        if enable_audio and self.tts_available:
            audio_bytes, audio_path = await self.text_to_speech(text, voice=voice)
            if audio_bytes:
                result["audio"] = audio_bytes
                result["audio_path"] = audio_path
                result["audio_available"] = True

        return result

    def format_response(self, response_text: str, include_history: bool = False) -> str:
        """
        Format response with optional conversation context

        Args:
            response_text: The response text
            include_history: Whether to include conversation history reference

        Returns:
            Formatted response string
        """
        if include_history and self.conversation_history:
            summary = self.get_history_summary()
            footer = f"\n\n---\n📊 *Conversation Turn {summary['total_turns']}* | Session: {summary['session_id'][:8]}"
            return response_text + footer

        return response_text

    async def stream_response_with_audio(
        self,
        text_generator,
        enable_audio: bool = True,
        voice: Optional[str] = None
    ):
        """
        Stream text response and generate audio when complete

        Args:
            text_generator: Generator yielding text chunks
            enable_audio: Whether to generate audio
            voice: Optional voice override

        Returns:
            Generator yielding (text_chunk, audio_data, is_complete)
        """
        full_response = ""

        # Stream the text
        async for chunk in text_generator:
            full_response += chunk
            yield chunk, None, False

        # Generate audio for complete response
        if enable_audio and self.tts_available:
            audio_result = await self.process_response_with_audio(full_response, enable_audio, voice)
            yield "", audio_result["audio"], True

    def get_voice_options(self) -> Dict[str, str]:
        """Get available voice options"""
        return self.available_voices

    def set_voice(self, voice_key: str):
        """Set voice by key"""
        if voice_key in self.available_voices:
            self.voice = self.available_voices[voice_key]
            return True
        return False


# Singleton instance
_conversation_agent = None

def get_conversation_agent() -> ConversationAgent:
    """Get or create conversation agent singleton"""
    global _conversation_agent
    if _conversation_agent is None:
        _conversation_agent = ConversationAgent()
    return _conversation_agent

def reset_conversation_agent():
    """Reset conversation agent"""
    global _conversation_agent
    _conversation_agent = ConversationAgent()
