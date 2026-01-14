"""
ProVerBs Ultimate Brain with Complete Voice Cloning
Integrates Supertonic voice cloning with all controls
"""

# Import everything from app_ultimate_brain
import sys
import os
sys.path.append(os.path.dirname(__file__))

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests

# Import Unified Brain
from unified_brain import UnifiedBrain, ReasoningContext

# Import Performance & Analytics
from performance_optimizer import performance_cache, performance_monitor, with_caching
from analytics_seo import analytics_tracker, SEOOptimizer

# Import Voice Cloning
from supertonic_voice_module import create_supertonic_interface

# Define class FIRST
class UltimateLegalBrain:
    def __init__(self):
        self.brain = UnifiedBrain()
        self.legal_modes = {
            "navigation": "📍 Navigation Guide",
            "general": "💬 General Legal",
            "document_validation": "📄 Document Validator",
            "legal_research": "🔍 Legal Research",
            "etymology": "📚 Etymology Expert",
            "case_management": "💼 Case Management",
            "regulatory_updates": "📋 Regulatory Updates"
        }
    
    async def process_legal_query(self, query: str, mode: str, ai_provider: str = "huggingface", use_reasoning_protocols: bool = True, **kwargs) -> Dict:
        reasoning_result = None
        if use_reasoning_protocols:
            preferences = {'use_reflection': mode in ['document_validation', 'legal_research'], 'multi_agent': False}
            reasoning_result = await self.brain.process(query=query, preferences=preferences, execution_mode='sequential')
        
        legal_prompt = self.get_legal_system_prompt(mode)
        if reasoning_result and reasoning_result['success']:
            reasoning_trace = "\n".join([f"🧠 {r['protocol']}: {', '.join(r['trace'][:2])}" for r in reasoning_result['results']])
            enhanced_query = f"{legal_prompt}\n\nReasoning Analysis:\n{reasoning_trace}\n\nUser Query: {query}"
        else:
            enhanced_query = f"{legal_prompt}\n\nUser Query: {query}"
        
        return {"enhanced_query": enhanced_query, "reasoning_result": reasoning_result, "mode": mode, "ai_provider": ai_provider}
    
    def get_legal_system_prompt(self, mode: str) -> str:
        prompts = {
            "navigation": "You are a ProVerBs Legal AI Navigation Guide with advanced reasoning capabilities.",
            "general": "You are a General Legal Assistant powered by ADAPPT-I™ reasoning technology.",
            "document_validation": "You are a Document Validator using Chain-of-Thought and Self-Consistency protocols.",
            "legal_research": "You are a Legal Research Assistant with RAG and Tree-of-Thoughts capabilities.",
            "etymology": "You are a Legal Etymology Expert with multi-step reasoning.",
            "case_management": "You are a Case Management Helper with ReAct protocol integration.",
            "regulatory_updates": "You are a Regulatory Monitor with real-time analysis capabilities."
        }
        return prompts.get(mode, prompts["general"])

async def respond_with_ultimate_brain(message, history: list, mode: str, ai_provider: str, use_reasoning: bool, max_tokens: int, temperature: float, top_p: float, hf_token = None):
    import time
    start_time = time.time()
    
    brain_result = await ultimate_brain.process_legal_query(query=message, mode=mode, ai_provider=ai_provider, use_reasoning_protocols=use_reasoning)
    
    if use_reasoning and brain_result['reasoning_result']:
        reasoning_info = "🧠 **Reasoning Protocols Applied:**\n"
        for r in brain_result['reasoning_result']['results']:
            reasoning_info += f"- {r['protocol']}: ✅ {r['status']}\n"
        yield reasoning_info + "\n\n"
    
    if ai_provider == "huggingface":
        token = hf_token.token if hf_token else None
        client = InferenceClient(token=token, model="meta-llama/Llama-3.3-70B-Instruct")
        
        messages = [{"role": "system", "content": brain_result['enhanced_query']}]
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": message})
        
        response = reasoning_info if use_reasoning and brain_result['reasoning_result'] else ""
        try:
            for chunk in client.chat_completion(messages, max_tokens=max_tokens, stream=True, temperature=temperature, top_p=top_p):
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    yield response
        except Exception as e:
            yield f"{response}\n\n❌ Error: {str(e)}"

# Custom CSS
custom_css = """
.gradio-container { max-width: 1400px !important; }
.header-section {
    text-align: center; padding: 40px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border-radius: 12px; margin-bottom: 30px;
}
.header-section h1 { font-size: 3rem; margin-bottom: 10px; font-weight: 700; }
.brain-badge {
    display: inline-block; background: #ff6b6b; color: white;
    padding: 8px 16px; border-radius: 20px; font-weight: bold;
    margin: 10px 5px;
}
"""

# SEO
seo_meta = SEOOptimizer.get_meta_tags()
seo_structured = SEOOptimizer.get_structured_data()

# Initialize AFTER class definition
ultimate_brain = UltimateLegalBrain()

# Override the demo with voice cloning integrated
demo_with_voice = gr.Blocks(title="ProVerBs Ultimate Legal AI Brain", css=custom_css)

with demo_with_voice:
    # Add SEO tags
    gr.HTML(seo_meta + seo_structured)
    
    # Header
    gr.HTML("""
    <div class="header-section">
        <h1>⚖️ ProVerBs Ultimate Legal AI Brain</h1>
        <p style="font-size: 1.3rem;">Powered by Pro'VerBs™ & ADAPPT-I™ Technology</p>
        <div>
            <span class="brain-badge">🧠 100+ Reasoning Protocols</span>
            <span class="brain-badge">🤖 6 AI Models</span>
            <span class="brain-badge">⚖️ 7 Legal Modes</span>
            <span class="brain-badge">🎙️ Voice Cloning</span>
        </div>
        <p style="font-size: 0.9rem; margin-top: 15px; opacity: 0.9;">
            Chain-of-Thought • Self-Consistency • Tree-of-Thoughts • ReAct • Reflexion • RAG<br>
            Quantum Reasoning • Multi-Agent • Voice Cloning • Audio Processing
        </p>
    </div>
    """)
    
    with gr.Tabs():
        # Welcome Tab
        with gr.Tab("🏠 Welcome"):
            gr.Markdown("""
            ## Welcome to the Ultimate ProVerBs Legal AI Brain
            
            ### 🧠 Unified Reasoning Brain (100+ Protocols)
            
            **Core Reasoning Protocols:**
            - Chain-of-Thought (CoT) - Step-by-step reasoning
            - Self-Consistency - Multiple reasoning paths
            - Tree-of-Thoughts (ToT) - Branching exploration
            - ReAct - Reason + Act cycles
            - Reflexion - Self-reflection with memory
            - RAG - Retrieval-Augmented Generation
            
            ### 🤖 6 AI Model Options:
            - 🤗 HuggingFace Llama-3.3-70B (Free, always available)
            - 🧠 GPT-4 Turbo (OpenAI)
            - ✨ Gemini 3.0 (Google)
            - 🔍 Perplexity AI (Research)
            - 🥷 Ninja AI
            - 💻 LM Studio (Local)
            
            ### ⚖️ 7 Specialized Legal Modes:
            - Navigation | General Legal | Document Validation
            - Legal Research | Etymology | Case Management | Regulatory Updates
            
            ### 🎙️ **NEW! Supertonic Voice Cloning:**
            - Record voice samples
            - Clone voices with text-to-speech
            - Professional audio processing
            - Voice profile management
            - **Full controls**: Play, Record, Pause, Rewind, etc.
            
            **Get Started:** Click "🤖 AI Legal Chatbot" or "🎙️ Voice Cloning" tab!
            """)
        
        # AI Chatbot Tab (copy from original)
        with gr.Tab("🤖 AI Legal Chatbot"):
            gr.Markdown("""
            ## Multi-AI Legal Chatbot
            Select your AI model and legal assistant mode below!
            """)
            
            with gr.Row():
                ai_provider_selector = gr.Dropdown(
                    choices=[
                        ("🤗 Llama-3.3-70B (Free)", "huggingface"),
                        ("🧠 GPT-4 Turbo", "gpt4"),
                        ("✨ Gemini 3.0", "gemini"),
                        ("🔍 Perplexity AI", "perplexity"),
                        ("🥷 Ninja AI", "ninjaai"),
                        ("💻 LM Studio", "lmstudio")
                    ],
                    value="huggingface",
                    label="🤖 AI Model"
                )
                
                mode_selector = gr.Dropdown(
                    choices=[
                        ("📍 Navigation", "navigation"),
                        ("💬 General Legal", "general"),
                        ("📄 Document Validator", "document_validation"),
                        ("🔍 Legal Research", "legal_research"),
                        ("📚 Etymology", "etymology"),
                        ("💼 Case Management", "case_management"),
                        ("📋 Regulatory Updates", "regulatory_updates")
                    ],
                    value="general",
                    label="⚖️ Legal Mode"
                )
                
                use_reasoning_toggle = gr.Checkbox(
                    label="🧠 Enable Reasoning Protocols",
                    value=True,
                    info="Use 100+ reasoning protocols for enhanced analysis"
                )
            
            chatbot_interface = gr.ChatInterface(
                respond_with_ultimate_brain,
                chatbot=gr.Chatbot(
                    height=550,
                    placeholder="💬 Ultimate Legal AI ready! Ask anything...",
                    show_label=False
                ),
                textbox=gr.Textbox(
                    placeholder="Ask your legal question here...",
                    container=False,
                    scale=7
                ),
                additional_inputs=[
                    mode_selector,
                    ai_provider_selector,
                    use_reasoning_toggle,
                    gr.Slider(128, 4096, value=2048, step=128, label="Max Tokens"),
                    gr.Slider(0.1, 2.0, value=0.7, step=0.1, label="Temperature"),
                    gr.Slider(0.1, 1.0, value=0.95, step=0.05, label="Top-p")
                ],
                examples=[
                    ["What reasoning protocols are available?"],
                    ["Analyze this contract using Chain-of-Thought reasoning"],
                    ["Research case law with Tree-of-Thoughts exploration"]
                ],
                cache_examples=False
            )
        
        # Voice Cloning Tab - FULL SUPERTONIC INTERFACE
        with gr.Tab("🎙️ Voice Cloning"):
            create_supertonic_interface()
        
        # Analytics Tab
        with gr.Tab("📊 Analytics"):
            gr.Markdown("""
            ## Analytics & Performance Dashboard
            View real-time analytics and performance metrics for the Ultimate Brain.
            """)
            
            with gr.Row():
                analytics_btn = gr.Button("📊 Refresh Analytics", variant="primary")
                clear_cache_btn = gr.Button("🗑️ Clear Cache", variant="secondary")
            
            analytics_output = gr.JSON(label="Analytics Data")
            performance_output = gr.JSON(label="Performance Metrics")
            cache_stats_output = gr.JSON(label="Cache Statistics")
            
            def get_analytics():
                return analytics_tracker.get_analytics()
            
            def get_performance():
                return performance_monitor.get_metrics()
            
            def get_cache_stats():
                return performance_cache.get_stats()
            
            def clear_cache_action():
                performance_cache.clear()
                return {"status": "Cache cleared successfully"}
            
            analytics_btn.click(
                fn=lambda: (get_analytics(), get_performance(), get_cache_stats()),
                outputs=[analytics_output, performance_output, cache_stats_output]
            )
            
            clear_cache_btn.click(
                fn=clear_cache_action,
                outputs=[cache_stats_output]
            )
        
        # Reasoning Brain Tab
        with gr.Tab("🧠 Reasoning Brain"):
            gr.Markdown("""
            ## Unified AI Reasoning Brain
            
            ### 📊 Protocol Categories:
            
            #### Core Reasoning (Protocols 1-50)
            - Chain-of-Thought, Self-Consistency, Tree-of-Thoughts
            - ReAct, Reflexion, RAG, and more
            
            #### Quantum-Specific (Protocols 51-100)
            - Quantum Job Orchestration, VQE, QAOA
            - Circuit Transpilation, Error Mitigation
            
            #### Multi-Agent (Protocols 73-100)
            - Multi-Agent Coordination
            - Contract Net Protocol
            """)
        
        # About Tab
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About ProVerBs Ultimate Legal AI Brain
            
            ### 🚀 Revolutionary Features:
            - **100+ Reasoning Protocols** - Most advanced reasoning system
            - **6 AI Models** - Choose the best for your needs
            - **7 Legal Modes** - Specialized for different legal tasks
            - **Voice Cloning** - Professional Supertonic integration
            - **Audio Processing** - Complete recording and playback controls
            
            ### 🎙️ Voice Cloning Features:
            - Record voice samples with full controls
            - Clone any voice with text-to-speech
            - Professional audio processing
            - Export voice profiles
            - Play, Pause, Record, Rewind, Stop controls
            
            ### 📚 Resources:
            - **Main Space**: https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
            - **Supertonic**: https://github.com/supertone-inc/supertonic
            - **Models**: https://huggingface.co/Supertone/supertonic
            
            ### ⚠️ Disclaimer:
            This platform provides general legal information only. Consult with a licensed attorney for specific legal matters.
            
            ---
            **Version 3.0.0 + Voice Cloning** | Built by Solomon7890
            """)
    
    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; padding: 20px;">
        <p><strong>⚖️ ProVerBs Ultimate Legal AI Brain v3.0 + Voice Cloning</strong></p>
        <p>Powered by Pro'VerBs™ & ADAPPT-I™ | 100+ Protocols | 6 AI Models | Voice Cloning</p>
        <p style="font-size: 0.85rem; color: #666;">
            © 2025 Solomon 8888 | Built with ❤️ for legal professionals worldwide
        </p>
    </div>
    """)

# Use the new demo with voice cloning
demo = demo_with_voice

if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
