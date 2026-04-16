# FastAPI Conversation Endpoints - Testing Guide

## Overview

Your ProVerBs Legal AI now has 3 new conversation endpoints:

1. **POST /api/conversation/process** - Process legal queries
2. **POST /api/conversation/audio** - Generate audio from text
3. **GET /api/conversation/status** - Health check

## Setup & Installation

### Step 1: Install Dependencies

```bash
cd Proverbs_Law_MainPage_Official
pip install -r requirements.txt
```

### Step 2: Set Environment Variables (Optional)

Create a `.env` file in the root directory:

```bash
# .env
OPENAI_API_KEY=your_key_if_using_gpt4
GOOGLE_API_KEY=your_key_if_using_gemini
HF_TOKEN=your_huggingface_token
```

### Step 3: Start FastAPI Backend

```bash
python main_api.py
```

Or with live reload:

```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 8080
```

You should see:
```
Uvicorn running on http://0.0.0.0:8080
```

## Testing Endpoints

### 1. Health Check (Simple Test)

```bash
curl http://localhost:8080/api/conversation/status
```

**Expected Response:**
```json
{
  "status": "online",
  "service": "conversation_agent",
  "tts_available": true,
  "available_voices": {
    "aria_us": "en-US-AriaNeural",
    "guy_us": "en-US-GuyNeural",
    "amber_us": "en-US-AmberNeural",
    "ana_es": "es-ES-ElviraNeural",
    "pierre_fr": "fr-FR-HenriNeural"
  }
}
```

---

### 2. Process Conversation Query

**Endpoint:** `POST /api/conversation/process`

**Basic Request:**

```bash
curl -X POST http://localhost:8080/api/conversation/process \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is habeas corpus?",
    "mode": "etymology",
    "ai_provider": "huggingface",
    "use_reasoning": true,
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

**Advanced Request (with reasoning):**

```bash
curl -X POST http://localhost:8080/api/conversation/process \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze this contract for legal validity",
    "mode": "document_validation",
    "ai_provider": "huggingface",
    "session_id": "session_123",
    "user_id": "user_456",
    "use_reasoning": true,
    "max_tokens": 1024,
    "temperature": 0.5,
    "top_p": 0.9
  }'
```

**Response:**

```json
{
  "success": true,
  "response": "Habeas corpus is a fundamental legal principle...",
  "reasoning": {
    "protocols_applied": [
      {
        "name": "Chain-of-Thought",
        "status": "completed",
        "results": ["Step 1: Define term", "Step 2: Explain origin", "Step 3: Modern application"]
      }
    ]
  },
  "session_id": "session_123",
  "mode": "etymology",
  "ai_provider": "huggingface"
}
```

---

### 3. Generate Audio

**Endpoint:** `POST /api/conversation/audio`

**Request:**

```bash
curl -X POST http://localhost:8080/api/conversation/audio \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Habeas corpus is a fundamental legal principle meaning you have the body.",
    "voice": "en-US-AriaNeural",
    "rate": 1.0,
    "pitch": 0
  }'
```

**Response:**

```json
{
  "success": true,
  "audio_path": "/tmp/proverbs_tts_20240115_123456.mp3",
  "message": "Audio generated successfully"
}
```

---

## Request/Response Models

### ConversationRequest

```typescript
{
  query: string;                    // User's legal question
  mode?: string;                    // "general" | "etymology" | "legal_research" | etc.
  ai_provider?: string;             // "huggingface" | "gpt4" | "gemini" | etc.
  session_id?: string;              // Optional session tracking
  user_id?: string;                 // Optional user tracking
  use_reasoning?: boolean;          // Enable 100+ reasoning protocols
  max_tokens?: number;              // Default: 1024
  temperature?: number;             // 0.1-2.0, default: 0.7
  top_p?: number;                   // 0.1-1.0, default: 0.95
  hf_token?: string;               // HuggingFace token if using that provider
}
```

### AudioRequest

```typescript
{
  text: string;                     // Text to convert to speech
  voice?: string;                   // Voice name, default: "en-US-AriaNeural"
  rate?: number;                    // 0.5-2.0, default: 1.0
  pitch?: number;                   // -20 to 20, default: 0
}
```

---

## Testing with Python (Recommended)

Create a file `test_api.py`:

```python
import requests
import json

API_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/api/conversation/status")
    print("✅ Health Check:", response.json())

def test_conversation():
    """Test conversation endpoint"""
    payload = {
        "query": "What is the difference between tort and crime?",
        "mode": "general",
        "ai_provider": "huggingface",
        "max_tokens": 512,
        "use_reasoning": True
    }
    
    response = requests.post(f"{API_URL}/api/conversation/process", json=payload)
    result = response.json()
    
    print("✅ Conversation Response:")
    print(f"Response: {result['response'][:100]}...")
    print(f"Reasoning Protocols: {len(result.get('reasoning', {}).get('protocols_applied', []))}")

def test_audio():
    """Test audio generation"""
    payload = {
        "text": "The legal system is complex and requires careful analysis.",
        "voice": "en-US-AriaNeural",
        "rate": 1.0
    }
    
    response = requests.post(f"{API_URL}/api/conversation/audio", json=payload)
    result = response.json()
    
    print("✅ Audio Generation:")
    print(f"Audio Path: {result.get('audio_path')}")
    print(f"Success: {result.get('success')}")

if __name__ == "__main__":
    print("🧪 Testing ProVerBs Conversation API...\n")
    
    try:
        test_health()
        print()
        test_conversation()
        print()
        test_audio()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

Run it:

```bash
python test_api.py
```

---

## Testing with Postman (Visual)

1. **Import Collection**
   - Open Postman
   - Click "File" → "New Collection"
   - Name: `ProVerBs Conversation API`

2. **Add Requests**

   **Request 1: Health Check**
   - Method: GET
   - URL: `http://localhost:8080/api/conversation/status`
   - Click "Send"

   **Request 2: Process Query**
   - Method: POST
   - URL: `http://localhost:8080/api/conversation/process`
   - Body → raw JSON:
   ```json
   {
     "query": "Explain constitutional law in simple terms",
     "mode": "general",
     "ai_provider": "huggingface"
   }
   ```
   - Click "Send"

   **Request 3: Generate Audio**
   - Method: POST
   - URL: `http://localhost:8080/api/conversation/audio`
   - Body → raw JSON:
   ```json
   {
     "text": "Constitutional law is the body of law that defines the structure and function of government.",
     "voice": "en-US-AriaNeural",
     "rate": 1.0
   }
   ```
   - Click "Send"

---

## Troubleshooting

### Error: "Module 'app' has no attribute 'ultimate_brain'"

**Solution:** Make sure `app.py` is properly initialized. The `ultimate_brain` is instantiated at the top of `app.py`.

```python
# In app.py (around line 105)
ultimate_brain = UltimateLegalBrain()
```

### Error: "edge_tts not installed"

**Solution:** Install it manually:

```bash
pip install edge-tts>=6.1.0
```

### Error: "HuggingFace token not provided"

**Solution:** Either:
1. Set `HF_TOKEN` environment variable
2. Or pass `hf_token` in the request
3. Or the token is already in your `.env` file

### Response is too slow

**Possible causes:**
- HuggingFace free tier is slow (it's a shared resource)
- First request takes longer (model loading)
- Large max_tokens value

**Solutions:**
- Reduce `max_tokens` to 256-512
- Use a faster provider if you have API keys
- Wait for model warm-up

---

## Next Steps

Once these endpoints are working:

1. ✅ **Week 1-2 Complete**: FastAPI endpoints ready
2. 🚀 **Week 3**: Build Next.js UI to call these endpoints
3. 🔐 **Week 4**: Add Firebase authentication and storage

---

## API Documentation

Full endpoint docs will be available at:
```
http://localhost:8080/docs
```

This is auto-generated by FastAPI/Swagger UI.

---

**Ready for Week 3? Build the Next.js frontend components!**
