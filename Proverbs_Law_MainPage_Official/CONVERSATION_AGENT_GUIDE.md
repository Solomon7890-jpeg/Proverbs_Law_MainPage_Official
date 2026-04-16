# 🎤 Conversation Agent with Text-to-Speech

## Overview

The **Conversation Agent** is a new interactive module added to the ProVerBs Legal AI application. It enables seamless question-and-answer interactions with automatic text-to-speech (read aloud) capabilities.

## Features

### 1. **Question & Answer Interface**
- Type or paste your legal questions
- Get intelligent responses from multiple AI providers
- Maintain conversation context across multiple exchanges

### 2. **Text-to-Speech (Read Aloud)**
- Automatically converts responses to speech
- Multiple voice options available
- Adjustable speech rate and pitch
- Powered by Microsoft Edge TTS (free, no API key required)

### 3. **Conversation Memory**
- Tracks all Q&A interactions in session
- Displays conversation statistics
- Shows number of turns, session ID, providers used
- One-click history reset

### 4. **Multi-AI Support**
- 🤗 Llama-3.3-70B (Free, HuggingFace)
- 🧠 GPT-4 Turbo (OpenAI)
- ✨ Gemini 3.0 (Google)
- 🔍 Perplexity AI (Research)

### 5. **Legal Mode Selection**
- 💬 General Legal
- 📍 Navigation
- 📄 Document Validator
- 🔍 Legal Research
- 📚 Etymology

## How to Use

### Step 1: Access the Conversation Agent Tab
Open the application and navigate to the **"🎤 Conversation Agent"** tab.

### Step 2: Configure Settings
- Select your preferred **AI Model** (default: HuggingFace Free)
- Choose a **Legal Mode** for specialized responses
- Check **"🔊 Read Response Aloud"** if you want audio output

### Step 3: Ask Your Question
1. Type your legal question in the **"❓ Your Question"** field
2. Click **"🎤 Ask & Listen"** button
3. Wait for response generation (typically 5-30 seconds)

### Step 4: Listen to Response
- Response text appears in the **📝 Response** section
- If audio is enabled, audio file appears in **🔊 Audio Response**
- Click the audio player to listen

### Step 5: Continue Conversation
- Ask follow-up questions - context is maintained
- Conversation history updates automatically
- Click **"🗑️ Clear History"** to start fresh

## Technical Implementation

### Files Added
1. **`conversation_agent.py`** - Core conversation agent module
2. **`requirements.txt`** - Updated with `edge-tts>=6.1.0`
3. **`app.py`** - New conversation agent tab and integration

### Conversation Agent Class

```python
from conversation_agent import get_conversation_agent

# Get agent instance
agent = get_conversation_agent()

# Add conversation turn
agent.add_turn(
    user_query="What is habeas corpus?",
    assistant_response="Habeas corpus is...",
    mode="etymology",
    ai_provider="huggingface"
)

# Get conversation context for follow-ups
context = agent.get_conversation_context(max_turns=5)

# Generate speech
audio_bytes, audio_path = await agent.text_to_speech(
    text="Your response text here",
    voice="en-US-AriaNeural"
)

# Get conversation statistics
stats = agent.get_history_summary()
```

### Available Voices

| Voice Key | Description |
|-----------|-------------|
| `aria_us` | Aria (US English) - Default |
| `guy_us` | Guy (US English) |
| `amber_us` | Amber (US English) |
| `ana_es` | Ana (Spanish) |
| `pierre_fr` | Pierre (French) |

## API Features

### Conversation Agent Methods

#### `add_turn(user_query, assistant_response, mode, ai_provider)`
Adds a conversation turn to history with timestamps.

#### `get_conversation_context(max_turns=5)`
Returns formatted context of last N conversation turns.

#### `clear_history()`
Clears all conversation history for current session.

#### `get_history_summary()`
Returns statistics: total turns, session ID, providers used, modes used.

#### `async text_to_speech(text, output_path=None, voice=None)`
Converts text to speech.
- **Parameters:**
  - `text`: Text to convert (max 2000 chars)
  - `output_path`: Optional file path to save audio
  - `voice`: Optional voice override
- **Returns:** Tuple of (audio_bytes, output_file_path)

#### `async process_response_with_audio(text, enable_audio=True, voice=None)`
Processes response and optionally generates audio.
- **Returns:** Dict with text, audio, audio_path, audio_available

## Audio Features

### Specifications
- **Format**: MP3
- **Quality**: High quality (128kbps+)
- **Language Support**: 100+ languages
- **Max Text Length**: 2000 characters per request
- **Processing Time**: ~2-5 seconds per response
- **API**: Microsoft Edge TTS (Free, no key required)

### Voice Controls
- **Speech Rate**: 0.5x to 2.0x (adjustable)
- **Pitch**: -20Hz to +20Hz (adjustable)
- **Languages**: Multiple language voices available

## Installation

### 1. Update Dependencies
```bash
pip install -r requirements.txt
```

Key new dependency:
```
edge-tts>=6.1.0
```

### 2. Run Application
```bash
python app.py
```

Then navigate to the **🎤 Conversation Agent** tab.

## Examples

### Example 1: Simple Question
```
Q: What is the difference between tort and crime?
A: [Legal explanation with 100+ reasoning protocols applied]
🔊 [Audio reads response aloud]
```

### Example 2: Document Validation
```
Select Legal Mode: "Document Validator"
Q: Is this contract valid?
A: [Chain-of-Thought analysis of contract validity]
🔊 [Response read aloud]
```

### Example 3: Legal Research
```
Select Legal Mode: "Legal Research"
Q: Research recent case law on intellectual property
A: [Tree-of-Thoughts exploration with research findings]
🔊 [Findings read aloud]
```

## Performance Notes

- **First Run**: May take 15-30 seconds as libraries initialize
- **Subsequent Runs**: 5-10 seconds per response
- **Audio Generation**: Additional 2-5 seconds (depends on response length)
- **Conversation History**: Stored in memory (cleared on reset)

## Troubleshooting

### Audio Not Playing
- Check browser audio settings
- Ensure "🔊 Read Response Aloud" is checked
- Try different browser (Chrome/Firefox recommended)

### Slow Response
- HuggingFace free model is shared - may be slow at peak times
- Try a faster provider (GPT-4, Gemini) if API key available
- Disable reasoning protocols for faster responses

### Audio Quality Issues
- Adjust speech rate slider (try 1.0 to 1.5)
- Use different voice option
- Reduce response length (under 500 words recommended)

### History Not Updating
- Click "🎤 Ask & Listen" button (not just Enter)
- Check browser console for errors
- Try clearing browser cache

## Integration with Unified Brain

The Conversation Agent integrates seamlessly with ProVerBs' Unified Brain:

- **Reasoning Protocols**: Automatically applied to legal queries
- **Legal Modes**: Context-aware responses for different legal scenarios
- **Multi-AI Support**: Leverage any configured AI provider
- **Performance Optimization**: Caching and optimization layer

## Future Enhancements

Potential features for future versions:

1. **Speech-to-Text Input** - Ask questions by voice
2. **Conversation Export** - Save Q&A history as PDF/JSON
3. **Custom Audio Settings** - Save preferred voice/rate
4. **Multi-language Support** - Questions/responses in different languages
5. **Conversation Branching** - Explore alternative answers
6. **Integration with RAG** - Pull legal documents for context

## License

© 2025 Solomon 8888. All Rights Reserved.

Part of **ProVerBs™ Legal AI** platform.

---

**Questions?** Check the Welcome tab for more information or consult the documentation.
