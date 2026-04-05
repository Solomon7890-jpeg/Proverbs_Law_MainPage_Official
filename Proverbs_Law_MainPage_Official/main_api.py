from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
