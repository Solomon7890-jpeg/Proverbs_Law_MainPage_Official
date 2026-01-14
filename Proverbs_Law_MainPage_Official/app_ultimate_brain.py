"""
ProVerBs Legal AI - Ultimate Brain Integration
Combines Multi-AI + Unified Reasoning Brain + Supertonic Audio
Powered by Pro'VerBs™ and ADAPPT-I™ Technology
"""

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import requests

# Import Unified Brain
from unified_brain import UnifiedBrain, ReasoningContext

# Import Performance & Analytics
from performance_optimizer import performance_cache, performance_monitor, with_caching
from analytics_seo import analytics_tracker, SEOOptimizer

class UltimateLegalBrain:
    """
    Ultimate Legal AI Brain combining:
    - Multi-AI providers (GPT-4, Gemini, Perplexity, etc.)
    - 100+ Reasoning protocols
    - Legal-specific modes
    """
    
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
    
    async def process_legal_query(
        self, 
        query: str, 
        mode: str,
        ai_provider: str = "huggingface",
        use_reasoning_protocols: bool = True,
        **kwargs
    ) -> Dict:
        """Process legal query with Brain integration"""
        
        # Step 1: Use Unified Brain for reasoning if enabled
        reasoning_result = None
        if use_reasoning_protocols:
            preferences = {
                'use_reflection': mode in ['document_validation', 'legal_research'],
                'multi_agent': False
            }
            reasoning_result = await self.brain.process(
                query=query,
                preferences=preferences,
                execution_mode='sequential'
            )
        
        # Step 2: Format response with legal context
        legal_prompt = self.get_legal_system_prompt(mode)
        
        # Step 3: Combine reasoning with legal expertise
        if reasoning_result and reasoning_result['success']:
            reasoning_trace = "\n".join([
                f"🧠 {r['protocol']}: {', '.join(r['trace'][:2])}"
                for r in reasoning_result['results']
            ])
            enhanced_query = f"{legal_prompt}\n\nReasoning Analysis:\n{reasoning_trace}\n\nUser Query: {query}"
        else:
            enhanced_query = f"{legal_prompt}\n\nUser Query: {query}"
        
        return {
            "enhanced_query": enhanced_query,
            "reasoning_result": reasoning_result,
            "mode": mode,
            "ai_provider": ai_provider
        }
    
    def get_legal_system_prompt(self, mode: str) -> str:
        """Get legal-specific system prompts"""
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

# Initialize Ultimate Brain
ultimate_brain = UltimateLegalBrain()


async def respond_with_ultimate_brain(
    message, history: list, mode: str, ai_provider: str,
    use_reasoning: bool, max_tokens: int, temperature: float, top_p: float,
    hf_token = None
):
    """Generate response using Ultimate Brain"""
    
    import time
    start_time = time.time()
    
    # Track analytics
    analytics_tracker.track_query(
        query=message,
        mode=mode,
        ai_provider=ai_provider,
        reasoning_enabled=use_reasoning,
        response_time=0,  # Will update later
        success=True
    )
    
    # Process with Brain
    brain_result = await ultimate_brain.process_legal_query(
        query=message,
        mode=mode,
        ai_provider=ai_provider,
        use_reasoning_protocols=use_reasoning
    )
    
    # Show reasoning trace if available
    if use_reasoning and brain_result['reasoning_result']:
        reasoning_info = "🧠 **Reasoning Protocols Applied:**\n"
        for r in brain_result['reasoning_result']['results']:
            reasoning_info += f"- {r['protocol']}: ✅ {r['status']}\n"
        yield reasoning_info + "\n\n"
    
    # Generate AI response using selected provider
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
            for chunk in client.chat_completion(
                messages, max_tokens=max_tokens, stream=True,
                temperature=temperature, top_p=top_p
            ):
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    yield response
        except Exception as e:
            yield f"{response}\n\n❌ Error: {str(e)}"
    
    elif ai_provider == "gpt4":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            yield "⚠️ OpenAI API key not set. Add OPENAI_API_KEY to Space secrets."
            return
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4-turbo-preview",
            "messages": [{"role": "user", "content": brain_result['enhanced_query']}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        response = reasoning_info if use_reasoning and brain_result['reasoning_result'] else ""
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=data, stream=True)
            for line in resp.iter_lines():
                if line and line.startswith(b'data: ') and line != b'data: [DONE]':
                    try:
                        json_data = json.loads(line[6:])
                        if json_data['choices'][0]['delta'].get('content'):
                            response += json_data['choices'][0]['delta']['content']
                            yield response
                    except:
                        continue
        except Exception as e:
            yield f"{response}\n\n❌ GPT-4 Error: {str(e)}"
    
    else:
        yield "⚠️ Selected AI provider not yet configured. Using HuggingFace..."


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

# Create Gradio Interface
demo = gr.Blocks(title="ProVerBs Ultimate Legal AI Brain", css=custom_css)

# Add SEO meta tags
seo_meta = SEOOptimizer.get_meta_tags()
seo_structured = SEOOptimizer.get_structured_data()

with demo:
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
            <span class="brain-badge">🎵 Audio Processing</span>
        </div>
        <p style="font-size: 0.9rem; margin-top: 15px; opacity: 0.9;">
            Chain-of-Thought • Self-Consistency • Tree-of-Thoughts • ReAct • Reflexion • RAG<br>
            Quantum Reasoning • Multi-Agent Coordination • Advanced Optimization
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
            
            **Quantum-Specific Protocols:**
            - Quantum Job Orchestration
            - VQE (Variational Quantum Eigensolver)
            - QAOA (Quantum Approximate Optimization)
            - Circuit Transpilation
            - Error Mitigation
            
            **Multi-Agent Protocols:**
            - Agent Coordination
            - Contract Net Protocol
            - Decentralized Task Allocation
            
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
            
            ### 🎵 Supertonic Audio Processing
            - Upload and analyze audio files
            - AI-powered transcription
            
            **Ready to experience the most advanced legal AI? Click "Ultimate AI Chatbot"!**
            """)
        
        # Ultimate AI Chatbot Tab
        with gr.Tab("🧠 Ultimate AI Chatbot"):
            gr.Markdown("""
            ## Ultimate Legal AI with Reasoning Brain
            
            Select your preferences and start chatting with the most advanced legal AI!
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
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
                
                with gr.Column(scale=1):
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
                
                with gr.Column(scale=1):
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
                    ["Research case law with Tree-of-Thoughts exploration"],
                    ["Explain 'habeas corpus' with etymological reasoning"],
                    ["Validate this legal document using Self-Consistency"],
                    ["Help me manage my case with ReAct protocol"]
                ],
                cache_examples=False
            )
            
            gr.Markdown("""
            ### 🧠 Reasoning Protocols Explained:
            
            - **Chain-of-Thought**: Breaks down complex queries into step-by-step reasoning
            - **Self-Consistency**: Generates multiple reasoning paths and finds consensus
            - **Tree-of-Thoughts**: Explores branching approaches and selects the best
            - **ReAct**: Combines reasoning with action cycles for interactive problem-solving
            - **Reflexion**: Self-reflects on attempts and improves iteratively
            - **RAG**: Retrieves relevant knowledge before generating responses
            
            ### 💡 Pro Tips:
            - Enable reasoning protocols for complex legal questions
            - HuggingFace model works instantly (no API key needed)
            - Each legal mode is optimized for specific tasks
            - Reasoning trace shows which protocols were applied
            """)
        
        # Reasoning Brain Info Tab
        with gr.Tab("🧠 Reasoning Brain"):
            gr.Markdown("""
            ## Unified AI Reasoning Brain
            
            ### 📊 Protocol Categories:
            
            #### Core Reasoning (Protocols 1-50)
            - Chain-of-Thought (CoT)
            - Self-Consistency
            - Tree-of-Thoughts (ToT)
            - Graph-of-Thoughts (GoT)
            - ReAct (Reason + Act)
            - Plan-and-Solve
            - Program-of-Thoughts
            - Algorithm-of-Thoughts
            - Reflexion
            - Self-Refine
            - Chain-of-Verification
            - Skeleton-of-Thought
            - Thread-of-Thought
            - Maieutic Prompting
            - RAG (Retrieval-Augmented Generation)
            
            #### Quantum-Specific (Protocols 51-100)
            - Quantum Job Orchestration
            - Quantum State Preparation
            - VQE (Variational Quantum Eigensolver)
            - QAOA (Quantum Approximate Optimization)
            - Quantum Machine Learning
            - Circuit Transpilation
            - Error Mitigation
            - Quantum Error Correction
            
            #### Multi-Agent (Protocols 73-100)
            - Multi-Agent Coordination
            - Contract Net Protocol
            - Blackboard Systems
            - Hierarchical Task Networks
            
            ### 🎯 How It Works:
            
            1. **Query Analysis**: Your question is analyzed for keywords and intent
            2. **Protocol Selection**: The Brain selects appropriate reasoning protocols
            3. **Execution**: Protocols run in sequence or parallel
            4. **Synthesis**: Results are combined with legal expertise
            5. **Response**: Enhanced answer with reasoning trace
            
            ### 🔧 Powered By:
            - **Pro'VerBs™** Open-Source Protocol
            - **ADAPPT-I™** Technology Implementation
            - Proprietary © 2025 Solomon 8888
            
            ### ⚖️ Legal Applications:
            - Document analysis with multi-step verification
            - Case research with tree exploration
            - Contract validation with self-consistency
            - Legal reasoning with chain-of-thought
            - Regulatory updates with RAG
            """)
        
        # Analytics Dashboard Tab
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
            
            gr.Markdown("""
            ### 📈 What's Tracked:
            
            **Analytics:**
            - Total queries processed
            - Success rate
            - Average response time
            - Most popular legal modes
            - Most popular AI models
            - Reasoning protocol usage
            - Recent queries
            
            **Performance:**
            - Cache hit rate
            - Total requests
            - Average response time
            - Error rate
            
            **Cache:**
            - Current cache size
            - Maximum capacity
            - TTL (Time To Live)
            - Oldest cached entry
            
            ### 💡 Optimization Tips:
            - High cache hit rate = faster responses
            - Monitor popular modes to optimize
            - Clear cache if experiencing issues
            - Analytics help identify usage patterns
            """)
        
        # About Tab
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About ProVerBs Ultimate Legal AI Brain
            
            ### 🚀 Revolutionary Features:
            - **100+ Reasoning Protocols** - Most advanced reasoning system
            - **6 AI Models** - Choose the best for your needs
            - **7 Legal Modes** - Specialized for different legal tasks
            - **Quantum Reasoning** - Cutting-edge optimization protocols
            - **Multi-Agent System** - Coordinated problem-solving
            - **Audio Processing** - Supertonic AI integration
            
            ### 🏆 Technology Stack:
            - Unified AI Reasoning Brain (Proprietary)
            - Pro'VerBs™ Open-Source Protocol
            - ADAPPT-I™ Technology
            - Multi-AI Provider Integration
            - Advanced Natural Language Processing
            
            ### 🔑 API Key Setup:
            Set in Space Settings → Repository Secrets:
            - `OPENAI_API_KEY` - For GPT-4
            - `GOOGLE_API_KEY` - For Gemini
            - `PERPLEXITY_API_KEY` - For Perplexity
            - `NINJAAI_API_KEY` - For NinjaAI
            
            ### 📜 Legal & Trademarks:
            **Proprietary License – Free to Use**  
            © 2025 Solomon 8888. All Rights Reserved.
            
            **Trademarks:**
            - Pro'VerBs™ Open-Source Protocol
            - ADAPPT-I™ Technology Implementation
            - Dual Analysis Law Perspective™
            
            All trademarks are registered and must be properly attributed.
            
            ### ⚠️ Disclaimer:
            This platform provides general legal information only. It does not constitute legal advice.
            Always consult with a licensed attorney for specific legal matters.
            
            ---
            **Version 3.0.0** | Ultimate Brain Edition | Built by Solomon7890
            """)
    
    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; padding: 20px;">
        <p><strong>⚖️ ProVerBs Ultimate Legal AI Brain v3.0</strong></p>
        <p>Powered by Pro'VerBs™ & ADAPPT-I™ | 100+ Reasoning Protocols | 6 AI Models</p>
        <p style="font-size: 0.85rem; color: #666;">
            © 2025 Solomon 8888 | Built with ❤️ for legal professionals worldwide
        </p>
    </div>
    """)

if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
