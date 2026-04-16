from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import asyncio
import os
import gradio as gr
from typing import List, Dict, Optional, Any
from expert_router import ExpertRouter
from status_correction_module import StatusCorrectionModule
from harmonic_sequencer import HarmonicSequencer

# Import the core reasoning brain and Gradio interface
from unified_brain import UnifiedBrain, ReasoningContext
from intelligence_discovery import ModelDiscoveryEngine
from conversation_agent import get_conversation_agent
from app import create_login_interface # Assuming app.py is refactored to export the block

app = FastAPI(title="ProVerBs Legal AI - Ultimate Brain API")

# Configure CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[List[str]] = []
    user_status: Optional[str] = "Commercial"
    expertise_level: Optional[str] = "Beginner"
    preferences: Optional[Dict] = None
    mode: str = "general"
    model: str = "huggingface"
    token: Optional[str] = None


# === NEW: Conversation Agent Models ===
class ConversationRequest(BaseModel):
    """Request for conversation processing"""
    query: str
    mode: str = "general"
    ai_provider: str = "huggingface"
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    use_reasoning: bool = True
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.95
    hf_token: Optional[str] = None


class AudioRequest(BaseModel):
    """Request for text-to-speech"""
    text: str
    voice: str = "en-US-AriaNeural"
    rate: float = 1.0
    pitch: int = 0

brain = UnifiedBrain()
discovery_engine = ModelDiscoveryEngine()
router = ExpertRouter()
corrector = StatusCorrectionModule()
sequencer = HarmonicSequencer()

# Mount the compiled Next.js 3D Frontend
# This directory is created during the Multi-Stage Docker Build
if os.path.exists("./frontend-dist"):
    app.mount("/", StaticFiles(directory="./frontend-dist", html=True), name="frontend")
else:
    print("⚠️ Warning: frontend-dist not found. Serving API only.")

@app.get("/api/health")
async def health_check():
    return {"status": "online", "brain_ready": True}

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Status-Aware AI Stream. 
    Calibrates reasoning based on 'Sovereign' vs 'Commercial' standing.
    """
    # 1. Harmonic Wave Sequencing
    sequenced_logic = sequencer.sequence_logic([{"result": experts}])
    sequencer.resequence_by_status(request.user_status or "commercial")
    harmonic_output = sequencer.get_final_harmonic_output()
    
    # 2. Trigger Status Correction if requested
    if "correct status" in request.message.lower() or "reclaim standing" in request.message.lower():
        correction_report = corrector.generate_correction_roadmap(request.user_status or "commercial")
        print(f"⚖️ Status Correction Roadmap Generated: {correction_report}")

    async def event_generator():
        try:
            # 1. Yield Reasoning Trace
            yield f"data: {json.dumps({'type': 'reasoning', 'content': 'Initializing Unified Brain reasoning...'})}\n\n"
            
            preferences = {
                'use_reflection': request.mode in ['document_validation', 'legal_research'],
                'multi_agent': False
            }
            
            # Simulate reasoning steps for the UI (real one is in brain.process)
            await asyncio.sleep(0.5)
            yield f"data: {json.dumps({'type': 'reasoning', 'content': 'Applying 100+ Reasoning Protocols (Chain-of-Thought)...'})}\n\n"
            
            # 2. Process with Brain
            # Note: For production, we'd wrap brain.process in a stream
            result = await brain.process(
                query=request.message,
                preferences=preferences
            )
            
            if result['success']:
                final_response = result['results'][-1]['trace'][-1]
                yield f"data: {json.dumps({'type': 'message', 'content': final_response})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'error', 'content': 'Brain processing failed.'})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# === NEW: Conversation Agent Endpoints ===

@app.post("/api/conversation/process")
async def process_conversation(request: ConversationRequest):
    """
    Process a conversation query with the Ultimate Legal Brain

    Returns:
    {
        "response": "text response",
        "reasoning": {...},
        "session_id": "session-id",
        "success": true
    }
    """
    try:
        from app import ultimate_brain
        from huggingface_hub import InferenceClient

        # Process with Ultimate Brain
        brain_result = await ultimate_brain.process_legal_query(
            query=request.query,
            mode=request.mode,
            ai_provider=request.ai_provider,
            use_reasoning_protocols=request.use_reasoning
        )

        # Generate response based on AI provider
        response_text = ""
        reasoning_info = {}

        if request.use_reasoning and brain_result.get('reasoning_result'):
            reasoning_info = {
                "protocols_applied": [
                    {
                        "name": r['protocol'],
                        "status": r['status'],
                        "results": r['trace'][:3]  # First 3 results
                    }
                    for r in brain_result['reasoning_result'].get('results', [])
                ]
            }

        # Call the selected AI provider
        if request.ai_provider == "huggingface":
            token = request.hf_token
            client = InferenceClient(token=token, model="meta-llama/Llama-3.3-70B-Instruct")

            messages = [{"role": "system", "content": brain_result['enhanced_query']}]
            messages.append({"role": "user", "content": request.query})

            try:
                for chunk in client.chat_completion(
                    messages,
                    max_tokens=request.max_tokens,
                    stream=True,
                    temperature=request.temperature,
                    top_p=request.top_p
                ):
                    if chunk.choices and chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"HuggingFace error: {str(e)}")

        else:
            # Placeholder for other providers
            response_text = f"[{request.ai_provider.upper()}] Response would be generated here"

        return {
            "success": True,
            "response": response_text,
            "reasoning": reasoning_info,
            "session_id": request.session_id,
            "mode": request.mode,
            "ai_provider": request.ai_provider
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/conversation/audio")
async def generate_audio(request: AudioRequest):
    """
    Generate audio from text using text-to-speech

    Returns:
    {
        "audio_path": "/tmp/audio_file.mp3",
        "success": true
    }
    """
    try:
        agent = get_conversation_agent()

        # Set voice and speech settings
        agent.voice = request.voice
        agent.rate = request.rate
        agent.pitch = request.pitch

        # Generate audio
        audio_bytes, audio_path = await agent.text_to_speech(request.text)

        if not audio_path:
            raise Exception("Failed to generate audio")

        return {
            "success": True,
            "audio_path": audio_path,
            "message": "Audio generated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation error: {str(e)}")


@app.get("/api/conversation/status")
async def conversation_status():
    """
    Health check for conversation service
    """
    agent = get_conversation_agent()
    return {
        "status": "online",
        "service": "conversation_agent",
        "tts_available": agent.tts_available,
        "available_voices": agent.get_voice_options()
    }

@app.post("/api/maintain/self-evolve")
async def self_evolve(background_tasks: BackgroundTasks):
    """
    Autonomous endpoint triggered by Cloud Scheduler.
    Checks for latest models and updates brain config.
    """
    def run_discovery():
        print("🚀 Starting autonomous model discovery...")
        models = discovery_engine.discover_latest_legal_models()
        # Save to config for next app reload
        with open("dynamic_models.json", "w") as f:
            json.dump(models, f)
        print(f"✅ Discovered {len(models)} new models.")

    background_tasks.add_task(run_discovery)
    return {"status": "Evolving...", "cycle": "24h"}

# Mount the Legacy Gradio UI for developers/internal use
# Ensure app.py has a function that returns the Blocks interface
try:
    from app import demo as gradio_demo
    app = gr.mount_gradio_app(app, gradio_demo, path="/gradio")
except Exception as e:
    print(f"⚠️ Could not mount Gradio UI: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
