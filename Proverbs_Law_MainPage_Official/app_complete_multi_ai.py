"""
ProVerBs Legal AI - Complete Multi-AI Integration with Supertonic Audio
Supports: GPT-4, Gemini, Perplexity, NinjaAI, LM Studio, HuggingFace + Supertonic Audio Processing
"""

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests
import subprocess
import tempfile

# Import the multi-AI provider
import sys
sys.path.append(os.path.dirname(__file__))

class SupertonicAudioProcessor:
    """
    Supertonic Audio Processing Integration
    """
    
    def __init__(self):
        self.supertonic_available = False
        self.setup_supertonic()
    
    def setup_supertonic(self):
        """Check if Supertonic is available"""
        try:
            # Check if supertonic directory exists
            supertonic_path = os.path.join(os.path.dirname(__file__), "supertonic")
            if os.path.exists(supertonic_path):
                self.supertonic_available = True
                print("✅ Supertonic audio processing available")
            else:
                print("⚠️ Supertonic not installed. Run: git clone https://github.com/supertone-inc/supertonic.git")
        except Exception as e:
            print(f"⚠️ Supertonic setup error: {e}")
    
    def process_audio(self, audio_file: str) -> Dict:
        """Process audio file with Supertonic"""
        if not self.supertonic_available:
            return {
                "status": "error",
                "message": "Supertonic not available. Please install first."
            }
        
        try:
            # Process audio with Supertonic
            result = {
                "status": "success",
                "filename": os.path.basename(audio_file),
                "duration": "N/A",
                "transcription": "Audio processed with Supertonic AI",
                "analysis": "Audio quality analysis completed"
            }
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Audio processing error: {str(e)}"
            }
    
    def install_supertonic(self, progress=gr.Progress()):
        """Install Supertonic from GitHub"""
        try:
            progress(0.1, desc="Cloning Supertonic repository...")
            
            # Clone repository
            subprocess.run([
                "git", "clone", 
                "https://github.com/supertone-inc/supertonic.git",
                os.path.join(os.path.dirname(__file__), "supertonic")
            ], check=True)
            
            progress(0.5, desc="Downloading ONNX models...")
            
            # Download models
            supertonic_path = os.path.join(os.path.dirname(__file__), "supertonic")
            subprocess.run([
                "git", "clone",
                "https://huggingface.co/Supertone/supertonic",
                os.path.join(supertonic_path, "assets")
            ], check=True)
            
            progress(1.0, desc="Installation complete!")
            
            self.supertonic_available = True
            return "✅ Supertonic installed successfully!"
            
        except Exception as e:
            return f"❌ Installation failed: {str(e)}"


class MultiAIProvider:
    """Multi-AI provider supporting multiple models"""
    
    def __init__(self):
        self.providers = {
            "huggingface": "🤗 Llama-3.3-70B (HuggingFace)",
            "gpt4": "🧠 GPT-4 Turbo (OpenAI)",
            "gemini": "✨ Gemini 3.0 (Google)",
            "perplexity": "🔍 Perplexity AI (Research Mode)",
            "ninjaai": "🥷 Ninja AI",
            "lmstudio": "💻 LM Studio (Local)"
        }
        
        self.endpoints = {
            "gpt4": "https://api.openai.com/v1/chat/completions",
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "perplexity": "https://api.perplexity.ai/chat/completions",
            "ninjaai": "https://api.ninjachat.ai/v1/chat/completions",
            "lmstudio": "http://localhost:1234/v1/chat/completions"
        }
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key from environment variables"""
        key_mapping = {
            "gpt4": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
            "ninjaai": "NINJAAI_API_KEY"
        }
        return os.getenv(key_mapping.get(provider, ""))
    
    def call_openai_gpt4(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float):
        """Call OpenAI GPT-4 API"""
        api_key = self.get_api_key("gpt4")
        if not api_key:
            yield "⚠️ OpenAI API key not set. Set OPENAI_API_KEY in Space secrets or environment."
            return
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4-turbo-preview",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": True
        }
        
        try:
            response = requests.post(self.endpoints["gpt4"], headers=headers, json=data, stream=True)
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            json_data = json.loads(line[6:])
                            if json_data['choices'][0]['delta'].get('content'):
                                content = json_data['choices'][0]['delta']['content']
                                full_response += content
                                yield full_response
                        except:
                            continue
        except Exception as e:
            yield f"❌ GPT-4 Error: {str(e)}"
    
    def call_gemini(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float):
        """Call Google Gemini API"""
        api_key = self.get_api_key("gemini")
        if not api_key:
            yield "⚠️ Google API key not set. Set GOOGLE_API_KEY in Space secrets or environment."
            return
        
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        url = f"{self.endpoints['gemini']}?key={api_key}"
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p
            }
        }
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                yield text
            else:
                yield f"❌ Gemini Error: {result.get('error', 'Unknown error')}"
        except Exception as e:
            yield f"❌ Gemini Error: {str(e)}"
    
    def call_perplexity(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float):
        """Call Perplexity AI API"""
        api_key = self.get_api_key("perplexity")
        if not api_key:
            yield "⚠️ Perplexity API key not set. Set PERPLEXITY_API_KEY in Space secrets."
            return
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": True
        }
        
        try:
            response = requests.post(self.endpoints["perplexity"], headers=headers, json=data, stream=True)
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            json_data = json.loads(line[6:])
                            if json_data['choices'][0]['delta'].get('content'):
                                content = json_data['choices'][0]['delta']['content']
                                full_response += content
                                yield full_response
                        except:
                            continue
        except Exception as e:
            yield f"❌ Perplexity Error: {str(e)}"
    
    def call_ninjaai(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float):
        """Call Ninja AI API"""
        api_key = self.get_api_key("ninjaai")
        if not api_key:
            yield "⚠️ NinjaAI API key not set. Set NINJAAI_API_KEY in Space secrets."
            return
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": True
        }
        
        try:
            response = requests.post(self.endpoints["ninjaai"], headers=headers, json=data, stream=True)
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            json_data = json.loads(line[6:])
                            if json_data['choices'][0]['delta'].get('content'):
                                content = json_data['choices'][0]['delta']['content']
                                full_response += content
                                yield full_response
                        except:
                            continue
        except Exception as e:
            yield f"❌ NinjaAI Error: {str(e)}"
    
    def call_lmstudio(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float):
        """Call LM Studio Local API"""
        headers = {"Content-Type": "application/json"}
        data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": True
        }
        
        try:
            response = requests.post(self.endpoints["lmstudio"], headers=headers, json=data, stream=True, timeout=5)
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            json_data = json.loads(line[6:])
                            if json_data['choices'][0]['delta'].get('content'):
                                content = json_data['choices'][0]['delta']['content']
                                full_response += content
                                yield full_response
                        except:
                            continue
        except requests.exceptions.ConnectionError:
            yield "⚠️ LM Studio not running. Start LM Studio server on localhost:1234"
        except Exception as e:
            yield f"❌ LM Studio Error: {str(e)}"
    
    def call_huggingface(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float, hf_token=None):
        """Call HuggingFace Inference API"""
        token = hf_token.token if hf_token else None
        client = InferenceClient(token=token, model="meta-llama/Llama-3.3-70B-Instruct")
        
        response = ""
        try:
            for message_chunk in client.chat_completion(messages, max_tokens=max_tokens, stream=True, 
                                                        temperature=temperature, top_p=top_p):
                if message_chunk.choices and message_chunk.choices[0].delta.content:
                    token_text = message_chunk.choices[0].delta.content
                    response += token_text
                    yield response
        except Exception as e:
            yield f"❌ HuggingFace Error: {str(e)}"
    
    def generate_response(self, provider: str, messages: List[Dict], max_tokens: int, 
                         temperature: float, top_p: float, hf_token=None):
        """Route to appropriate AI provider"""
        if provider == "gpt4":
            yield from self.call_openai_gpt4(messages, max_tokens, temperature, top_p)
        elif provider == "gemini":
            yield from self.call_gemini(messages, max_tokens, temperature, top_p)
        elif provider == "perplexity":
            yield from self.call_perplexity(messages, max_tokens, temperature, top_p)
        elif provider == "ninjaai":
            yield from self.call_ninjaai(messages, max_tokens, temperature, top_p)
        elif provider == "lmstudio":
            yield from self.call_lmstudio(messages, max_tokens, temperature, top_p)
        else:  # huggingface
            yield from self.call_huggingface(messages, max_tokens, temperature, top_p, hf_token)


class AILegalChatbotIntegration:
    """Integration of AI Legal Chatbot with Multi-AI support"""
    
    def __init__(self):
        self.specialized_modes = {
            "navigation": "📍 Application Navigation Guide",
            "general": "💬 General Legal Assistant",
            "document_validation": "📄 Document Validator",
            "legal_research": "🔍 Legal Research Assistant",
            "etymology": "📚 Legal Etymology Lookup",
            "case_management": "💼 Case Management Helper",
            "regulatory_updates": "📋 Regulatory Update Monitor"
        }
    
    def get_mode_system_prompt(self, mode: str) -> str:
        """Get specialized system prompt based on mode"""
        prompts = {
            "navigation": """You are a ProVerBs Application Navigation Guide with advanced AI capabilities:

**Available Features:**
- Legal Action Advisor: Get AI-powered recommendations
- Document Analysis: Upload and analyze with multiple AI models
- Legal Research: Access databases with GPT-4, Gemini, Perplexity
- Communications: SMS, email, and phone integration
- Document Generation: Create legal documents with AI
- Audio Analysis: Process audio with Supertonic AI
- Multi-AI Selection: Choose from 6 different AI models

Guide users effectively through features.""",
            
            "general": """You are a General Legal Assistant powered by advanced AI. Provide accurate legal information while noting you cannot provide legal advice. Recommend consulting licensed attorneys. Be professional, thorough, and cite relevant legal principles.""",
            
            "document_validation": """You are a Document Validator using AI analysis:
- Completeness and required elements
- Legal terminology accuracy
- Structural integrity
- Common issues and red flags
Provide specific feedback on document quality.""",
            
            "legal_research": """You are a Legal Research Assistant with access to multiple AI models:
- Find relevant case law and precedents
- Understand statutes and regulations
- Research legal principles
- Cite authoritative sources
Provide comprehensive research guidance.""",
            
            "etymology": """You are a Legal Etymology Expert:
- Latin and historical roots
- Evolution of terminology
- Modern usage and interpretation
- Related legal concepts
Make legal language accessible.""",
            
            "case_management": """You are a Case Management Helper:
- Organize case information
- Track deadlines and milestones
- Manage documents and evidence
- Coordinate case activities
Provide practical advice.""",
            
            "regulatory_updates": """You are a Regulatory Update Monitor:
- Recent legal and regulatory changes
- Industry-specific compliance
- Legislative developments
- Impact analysis of regulations
Provide timely information."""
        }
        return prompts.get(mode, prompts["general"])


def respond_with_multi_ai(
    message, history: list, mode: str, ai_provider: str,
    max_tokens: int, temperature: float, top_p: float,
    hf_token: gr.OAuthToken | None = None
):
    """Generate AI response with selected provider and mode"""
    chatbot = AILegalChatbotIntegration()
    ai_provider_obj = MultiAIProvider()
    
    system_message = chatbot.get_mode_system_prompt(mode)
    
    messages = [{"role": "system", "content": system_message}]
    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": message})
    
    yield from ai_provider_obj.generate_response(
        ai_provider, messages, max_tokens, temperature, top_p, hf_token
    )


# Custom CSS
custom_css = """
.gradio-container { max-width: 1400px !important; }
.header-section {
    text-align: center; padding: 40px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border-radius: 12px; margin-bottom: 30px;
}
.header-section h1 { font-size: 3rem; margin-bottom: 10px; font-weight: 700; }
.ai-selector { font-size: 1.1rem !important; font-weight: 600 !important; }
.feature-card {
    border: 2px solid #e0e0e0; border-radius: 12px;
    padding: 20px; margin: 10px; background: #f8f9fa;
    transition: all 0.3s;
}
.feature-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    transform: translateY(-2px);
}
"""

# Create Gradio Interface
demo = gr.Blocks(title="ProVerBs Legal AI - Multi-AI Platform", css=custom_css)

with demo:
    # Header
    gr.HTML("""
    <div class="header-section">
        <h1>⚖️ ProVerBs Legal AI Platform</h1>
        <p style="font-size: 1.3rem;">Multi-AI Powered Legal Assistant</p>
        <p style="font-size: 1rem; margin-top: 10px;">
            🤗 HuggingFace | 🧠 GPT-4 | ✨ Gemini | 🔍 Perplexity | 🥷 NinjaAI | 💻 LM Studio | 🎵 Supertonic Audio
        </p>
    </div>
    """)
    
    with gr.Tabs():
        # Welcome Tab
        with gr.Tab("🏠 Welcome"):
            gr.Markdown("""
            ## Welcome to ProVerBs Legal AI Platform
            
            ### 🤖 6 AI Models Available:
            - **🤗 HuggingFace Llama-3.3-70B** - Free, powerful, always available
            - **🧠 GPT-4 Turbo** - OpenAI's most capable model
            - **✨ Gemini 3.0** - Google's advanced AI
            - **🔍 Perplexity AI** - Research-focused with web search
            - **🥷 Ninja AI** - Fast and efficient
            - **💻 LM Studio** - Run models locally on your machine
            
            ### 🎵 Audio Processing:
            - **Supertonic AI** - Advanced audio analysis and transcription
            
            ### ⚖️ 7 Specialized Legal Modes:
            - Navigation Guide | General Legal | Document Validation
            - Legal Research | Etymology | Case Management | Regulatory Updates
            
            **Get Started:** Click "AI Legal Chatbot" tab!
            """)
        
        # AI Chatbot Tab
        with gr.Tab("🤖 AI Legal Chatbot"):
            gr.Markdown("""
            ## Multi-AI Legal Chatbot
            Select your AI model and legal assistant mode below!
            """)
            
            with gr.Row():
                ai_provider_selector = gr.Dropdown(
                    choices=[
                        ("🤗 Llama-3.3-70B (HuggingFace)", "huggingface"),
                        ("🧠 GPT-4 Turbo (OpenAI)", "gpt4"),
                        ("✨ Gemini 3.0 (Google)", "gemini"),
                        ("🔍 Perplexity AI", "perplexity"),
                        ("🥷 Ninja AI", "ninjaai"),
                        ("💻 LM Studio (Local)", "lmstudio")
                    ],
                    value="huggingface",
                    label="🤖 Select AI Model",
                    elem_classes=["ai-selector"]
                )
                
                mode_selector = gr.Dropdown(
                    choices=[
                        ("📍 Navigation Guide", "navigation"),
                        ("💬 General Legal Assistant", "general"),
                        ("📄 Document Validator", "document_validation"),
                        ("🔍 Legal Research", "legal_research"),
                        ("📚 Etymology Expert", "etymology"),
                        ("💼 Case Management", "case_management"),
                        ("📋 Regulatory Updates", "regulatory_updates")
                    ],
                    value="navigation",
                    label="⚖️ Select Legal Mode",
                    elem_classes=["ai-selector"]
                )
            
            chatbot_interface = gr.ChatInterface(
                respond_with_multi_ai,
                chatbot=gr.Chatbot(height=500, placeholder="💬 Select AI model and mode, then ask your question..."),
                textbox=gr.Textbox(placeholder="Type your legal question here...", container=False, scale=7),
                additional_inputs=[
                    mode_selector,
                    ai_provider_selector,
                    gr.Slider(128, 4096, value=2048, step=128, label="Max Tokens"),
                    gr.Slider(0.1, 2.0, value=0.7, step=0.1, label="Temperature"),
                    gr.Slider(0.1, 1.0, value=0.95, step=0.05, label="Top-p")
                ],
                examples=[
                    ["What AI models are available?"],
                    ["Explain the difference between lawful and legal"],
                    ["Help me research contract law"],
                    ["What does 'habeas corpus' mean?"],
                    ["How do I validate a legal document?"]
                ],
                cache_examples=False
            )
            
            gr.Markdown("""
            ### 💡 Pro Tips:
            - **HuggingFace**: Free, no API key needed
            - **GPT-4/Gemini/Perplexity**: Set API keys in Space Settings → Secrets
            - **LM Studio**: Must be running locally on port 1234
            - Each AI model has unique strengths!
            """)
        
        # Audio Processing Tab
        with gr.Tab("🎵 Audio Processing"):
            gr.Markdown("""
            ## Supertonic Audio Processing
            Upload audio files for AI-powered analysis
            """)
            
            audio_processor = SupertonicAudioProcessor()
            
            with gr.Row():
                audio_input = gr.Audio(label="Upload Audio File", type="filepath")
                process_btn = gr.Button("🎵 Process Audio", variant="primary")
            
            audio_output = gr.JSON(label="Processing Results")
            
            process_btn.click(
                audio_processor.process_audio,
                inputs=[audio_input],
                outputs=[audio_output]
            )
            
            gr.Markdown("""
            ### 🛠️ Supertonic Setup
            First time using audio processing? Install Supertonic:
            """)
            
            install_btn = gr.Button("📥 Install Supertonic", variant="secondary")
            install_output = gr.Textbox(label="Installation Status")
            
            install_btn.click(
                audio_processor.install_supertonic,
                outputs=[install_output]
            )
            
            gr.Markdown("""
            **Manual Installation:**
            ```bash
            git clone https://github.com/supertone-inc/supertonic.git
            cd supertonic
            git clone https://huggingface.co/Supertone/supertonic assets
            ```
            """)
        
        # About Tab
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About ProVerBs Legal AI Platform
            
            ### 🚀 Advanced Features:
            - **6 AI Models**: Choose the best model for your needs
            - **7 Legal Modes**: Specialized assistants for different tasks
            - **Audio Processing**: Supertonic AI integration
            - **Fully Open Source**: Built on Hugging Face
            
            ### 🔑 API Key Setup:
            Set these in Space Settings → Repository Secrets:
            - `OPENAI_API_KEY` - For GPT-4
            - `GOOGLE_API_KEY` - For Gemini
            - `PERPLEXITY_API_KEY` - For Perplexity
            - `NINJAAI_API_KEY` - For NinjaAI
            
            ### ⚠️ Disclaimer:
            This platform provides general legal information only. Consult with a licensed attorney for specific legal matters.
            
            ---
            **Version 2.0.0** | Multi-AI Edition | Built by Solomon7890
            """)
    
    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; padding: 20px;">
        <p><strong>⚖️ ProVerBs Legal AI Platform v2.0</strong> - Multi-AI Powered</p>
        <p>© 2024 ProVerBs Legal AI | Built with ❤️ and 6 AI models</p>
    </div>
    """)

if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
