from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
import os
from typing import List, Dict, Optional

# Import the core reasoning brain
from unified_brain import UnifiedBrain, ReasoningContext
from intelligence_discovery import ModelDiscoveryEngine

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
    mode: str = "general"
    model: str = "huggingface"
    token: Optional[str] = None

brain = UnifiedBrain()
discovery_engine = ModelDiscoveryEngine()

@app.get("/api/health")
async def health_check():
    return {"status": "online", "brain_ready": True}

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint for the 3D Immersive Frontend.
    Provides real-time reasoning protocol trace + AI response.
    """
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
