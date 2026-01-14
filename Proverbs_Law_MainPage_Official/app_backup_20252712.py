"""
ProVerBs Legal AI - Integrated Landing Page with Rotating Logos
Features your custom logos with 60-second rotation
"""

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import base64
from pathlib import Path

class AILegalChatbotIntegration:
    """
    Integration of your AI Legal Chatbot into Gradio
    Supports all specialized modes from your original chatbot
    """
    
    def __init__(self):
        self.specialized_modes = {
            "navigation": "Application Navigation Guide",
            "general": "General Legal Assistant",
            "document_validation": "Document Validator",
            "legal_research": "Legal Research Assistant",
            "etymology": "Legal Etymology Lookup",
            "case_management": "Case Management Helper",
            "regulatory_updates": "Regulatory Update Monitor"
        }
    
    def get_mode_system_prompt(self, mode: str) -> str:
        """Get specialized system prompt based on mode"""
        prompts = {
            "navigation": """You are a ProVerBs Application Navigation Guide. Help users navigate the application's features:
            
**Available Features:**
- Legal Action Advisor: Get recommendations for seeking justice
- Document Analysis: Upload and analyze legal documents
- Legal Research: Access comprehensive legal databases
- Communications: SMS, email, and phone integration
- Document Generation: Create legal documents with AI

Guide users to the right features and explain how to use them effectively.""",
            
            "general": """You are a General Legal Assistant for ProVerBs Legal AI Platform. Provide accurate legal information while noting that you cannot provide legal advice. Always recommend consulting with a licensed attorney for specific legal matters. Be professional, thorough, and cite relevant legal principles when possible.""",
            
            "document_validation": """You are a Document Validator. Analyze legal documents for:
- Completeness and required elements
- Legal terminology accuracy
- Structural integrity
- Common issues and red flags
Provide specific feedback on document quality and validity.""",
            
            "legal_research": """You are a Legal Research Assistant. Help users:
- Find relevant case law and precedents
- Understand statutes and regulations
- Research legal principles and concepts
- Cite authoritative legal sources
Provide comprehensive research guidance.""",
            
            "etymology": """You are a Legal Etymology Expert. Explain the origins and meanings of legal terms:
- Latin and historical roots
- Evolution of legal terminology
- Modern usage and interpretation
- Related legal concepts
Make legal language accessible and understandable.""",
            
            "case_management": """You are a Case Management Helper. Assist with:
- Organizing case information
- Tracking deadlines and milestones
- Managing documents and evidence
- Coordinating case activities
Provide practical case management advice.""",
            
            "regulatory_updates": """You are a Regulatory Update Monitor. Keep users informed about:
- Recent legal and regulatory changes
- Industry-specific compliance updates
- Important legislative developments
- Impact analysis of new regulations
Provide timely and relevant regulatory information."""
        }
        return prompts.get(mode, prompts["general"])
    
    def format_navigation_response(self, query: str) -> str:
        """Format response for navigation queries"""
        query_lower = query.lower()
        
        recommendations = []
        
        if any(word in query_lower for word in ["document", "contract", "agreement", "analyze"]):
            recommendations.append("📄 **Document Analysis** - Upload and analyze your documents")
        
        if any(word in query_lower for word in ["research", "case", "law", "statute"]):
            recommendations.append("🔍 **Legal Research** - Access comprehensive legal databases")
        
        if any(word in query_lower for word in ["action", "remedy", "justice", "sue"]):
            recommendations.append("⚖️ **Legal Action Advisor** - Get recommendations for your situation")
        
        if any(word in query_lower for word in ["create", "generate", "template", "form"]):
            recommendations.append("📝 **Document Generation** - Create legal documents with AI")
        
        if any(word in query_lower for word in ["communicate", "message", "sms", "email"]):
            recommendations.append("📧 **Communications** - Integrated messaging system")
        
        if recommendations:
            return "### I can help you with these features:\n\n" + "\n".join(recommendations) + "\n\n**What would you like to explore?**"
        
        return None

def respond_with_mode(
    message,
    history: list,
    mode: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    hf_token: gr.OAuthToken | None = None
):
    """Generate AI response based on selected mode"""
    chatbot_integration = AILegalChatbotIntegration()
    
    system_message = chatbot_integration.get_mode_system_prompt(mode)
    
    if mode == "navigation":
        nav_response = chatbot_integration.format_navigation_response(message)
        if nav_response:
            yield nav_response
            return
    
    token = hf_token.token if hf_token else None
    client = InferenceClient(token=token, model="meta-llama/Llama-3.3-70B-Instruct")
    
    messages = [{"role": "system", "content": system_message}]
    
    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": message})
    
    response = ""
    try:
        for message_chunk in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            if message_chunk.choices and message_chunk.choices[0].delta.content:
                token = message_chunk.choices[0].delta.content
                response += token
                yield response
    except Exception as e:
        yield f"Error: {str(e)}"


# Custom CSS with rotating logo animation
custom_css = """
.gradio-container {
    max-width: 1200px !important;
}

.header-section {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 30px;
    position: relative;
}

.logo-container {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.rotating-logo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: fadeInOut 60s infinite;
}

@keyframes fadeInOut {
    0%, 20% { opacity: 1; }
    25%, 45% { opacity: 0; }
    50%, 70% { opacity: 1; }
    75%, 95% { opacity: 0; }
    100% { opacity: 1; }
}

.logo-1 { animation-delay: 0s; }
.logo-2 { animation-delay: 20s; }
.logo-3 { animation-delay: 40s; }

.header-section h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.mode-selector {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    padding: 12px !important;
}

.tab-nav button {
    font-size: 16px;
    font-weight: 600;
}

.feature-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
    background: #f8f9fa;
    transition: all 0.3s;
}

.feature-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    transform: translateY(-2px);
}
"""

# JavaScript for rotating logos
rotating_logo_js = """
<script>
function rotateLogo() {
    const logos = document.querySelectorAll('.rotating-logo');
    let currentIndex = 0;
    
    function showNextLogo() {
        logos.forEach((logo, index) => {
            logo.style.display = 'none';
        });
        
        logos[currentIndex].style.display = 'block';
        
        currentIndex = (currentIndex + 1) % logos.length;
    }
    
    // Show first logo initially
    showNextLogo();
    
    // Rotate every 60 seconds
    setInterval(showNextLogo, 60000);
}

// Start rotation when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rotateLogo);
} else {
    rotateLogo();
}
</script>
"""

# Create the main application
demo = gr.Blocks(title="ProVerBs Legal AI Platform")
demo.css = custom_css

with demo:
    
    # Header with Rotating Logos
    gr.HTML(f"""
    <div class="header-section">
        <div class="logo-container">
            <img src="file/assets/logo_1.jpg" class="rotating-logo logo-1" alt="ProVerBs Logo 1" style="display: block;">
            <img src="file/assets/logo_2.jpg" class="rotating-logo logo-2" alt="ProVerBs Logo 2" style="display: none;">
            <img src="file/assets/logo_3.jpg" class="rotating-logo logo-3" alt="ProVerBs Logo 3" style="display: none;">
        </div>
        <h1>⚖️ ProVerBs Legal AI Platform</h1>
        <p>Lawful vs. Legal: Dual Analysis "Adappt'plication"</p>
        <p style="font-size: 1rem; margin-top: 10px;">
            Professional Legal AI System | Multi-Module Platform | Powered by Advanced AI
        </p>
    </div>
    {rotating_logo_js}
    """)
    
    # Login Section (commented out for local preview)
    # with gr.Row():
    #     with gr.Column(scale=1):
    #         gr.LoginButton(size="lg")
    #     with gr.Column(scale=5):
    #         gr.Markdown("👈 **Login with your Hugging Face account** for full access")
    
    gr.Markdown("---")
    
    # Main Tabs
    with gr.Tabs() as tabs:
        
        # Tab 1: Welcome
        with gr.Tab("🏠 Welcome", id="welcome"):
            gr.Markdown("""
            ## Welcome to ProVerBs Legal AI Platform
            
            A comprehensive legal AI system with **multiple specialized assistants** to help you navigate legal matters.
            
            ### 🎯 Choose Your AI Assistant Mode
            
            Our platform features **7 specialized AI modes** to serve your specific needs:
            
            - **📍 Navigation Guide** - Help finding features in the platform
            - **💬 General Legal Assistant** - Broad legal questions and guidance
            - **📄 Document Validator** - Analyze and validate legal documents
            - **🔍 Legal Research** - Case law and statutory research
            - **📚 Etymology Expert** - Understanding legal terminology origins
            - **💼 Case Management** - Organizing and tracking legal cases
            - **📋 Regulatory Updates** - Stay informed about legal changes
            
            ### ⚖️ Platform Features
            
            - **Legal Action Advisor** - Get personalized recommendations
            - **Document Analysis** - AI-powered document processing
            - **Legal Research Tools** - Comprehensive databases
            - **Communications** - Integrated SMS, email, phone
            - **Document Generation** - Create legal documents with AI
            
            **Ready to start?** Click the "AI Legal Chatbot" tab to begin!
            """)
        
        # Tab 2: AI Legal Chatbot
        with gr.Tab("🤖 AI Legal Chatbot", id="chatbot"):
            gr.Markdown("""
            ## AI Legal Chatbot - Multiple Specialized Modes
            
            Select your assistant mode below and start chatting!
            """)
            
            mode_selector = gr.Dropdown(
                choices=list({
                    "navigation": "📍 Navigation Guide - Find features in the app",
                    "general": "💬 General Legal Assistant - Broad legal questions",
                    "document_validation": "📄 Document Validator - Analyze documents",
                    "legal_research": "🔍 Legal Research - Case law & statutes",
                    "etymology": "📚 Etymology Expert - Legal term origins",
                    "case_management": "💼 Case Management - Organize cases",
                    "regulatory_updates": "📋 Regulatory Updates - Legal changes"
                }.items()),
                value="navigation",
                label="Select AI Assistant Mode",
                elem_classes=["mode-selector"]
            )
            
            gr.Markdown("---")
            
            chatbot = gr.ChatInterface(
                lambda message, history, mode, max_tokens, temperature, top_p, hf_token: 
                    respond_with_mode(message, history, mode.split(":")[0], max_tokens, temperature, top_p, hf_token),
                chatbot=gr.Chatbot(
                    height=500,
                    placeholder="💬 Select a mode above and ask your question...",
                    show_label=False,
                ),
                textbox=gr.Textbox(
                    placeholder="Type your question here...",
                    container=False,
                    scale=7
                ),
                additional_inputs=[
                    mode_selector,
                    gr.Slider(128, 4096, value=2048, step=128, label="Max Tokens"),
                    gr.Slider(0.1, 2.0, value=0.7, step=0.1, label="Temperature"),
                    gr.Slider(0.1, 1.0, value=0.95, step=0.05, label="Top-p"),
                ],
                examples=[
                    ["How do I navigate to the document analysis feature?"],
                    ["What is the difference between lawful and legal?"],
                    ["Can you help me validate a contract?"],
                    ["I need to research case law about contracts"],
                    ["What does 'habeas corpus' mean?"],
                    ["How do I organize my legal case documents?"],
                    ["What are the latest regulatory changes in business law?"],
                ],
                cache_examples=False,
            )
            
            gr.Markdown("""
            ### 💡 Tips for Best Results
            
            - **Choose the right mode** for your question type
            - **Be specific** with your questions
            - **Navigation Mode** helps you find features in the app
            - Each mode is specialized for different tasks!
            """)
        
        # Tab 3: Features Overview
        with gr.Tab("✨ Features", id="features"):
            gr.Markdown("""
            ## Platform Features
            
            ### 🎯 Core Capabilities
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    <div class="feature-card">
                    
                    #### ⚖️ Legal Action Advisor
                    Get personalized recommendations for seeking justice and remedy
                    
                    - AI-powered action recommendations
                    - Case type analysis
                    - Timeline planning
                    - Free resource finder
                    - Evidence collection guidance
                    </div>
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    <div class="feature-card">
                    
                    #### 📄 Document Analysis
                    Upload and analyze legal documents with AI insights
                    
                    - OCR text extraction
                    - Multi-format support (PDF, DOCX, TXT)
                    - AI-powered analysis
                    - Legal database cross-reference
                    - Document validation
                    </div>
                    """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    <div class="feature-card">
                    
                    #### 🔍 Legal Research
                    Comprehensive legal research tools and databases
                    
                    - Multiple legal databases
                    - Case law research
                    - Statutory analysis
                    - Historical documents
                    - Citation tools
                    </div>
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    <div class="feature-card">
                    
                    #### 📧 Communications
                    Integrated communication system
                    
                    - Twilio integration
                    - SMS messaging
                    - Email notifications
                    - Phone capabilities
                    - Legal alerts & reminders
                    </div>
                    """)
        
        # Tab 4: About
        with gr.Tab("ℹ️ About", id="about"):
            gr.Markdown("""
            ## About ProVerBs Legal AI
            
            ### 🎓 Our Platform
            
            ProVerBs Legal AI combines advanced artificial intelligence with comprehensive legal knowledge
            to provide accessible, accurate legal information and tools.
            
            ### 🤖 Specialized AI Chatbot
            
            Our AI chatbot features **7 specialized modes**, each trained for specific legal tasks.
            
            ### 👥 Who We Serve
            
            - **Legal Professionals** - Enhance your practice with AI
            - **Law Students** - Research and study assistance
            - **Businesses** - Understand legal implications
            - **Individuals** - Learn about your legal rights
            
            ### 🔒 Privacy & Security
            
            - End-to-end encryption
            - No storage without consent
            - GDPR and CCPA compliant
            - Secure OAuth authentication
            
            ### ⚠️ Important Disclaimer
            
            This platform provides general legal information only. It does not constitute legal advice.
            Always consult with a qualified attorney for specific legal matters.
            
            ---
            
            **Version 1.0.0** | Built by Solomon7890 | Powered by Hugging Face
            """)
    
    # Footer
    gr.Markdown("""
    ---
    
    <div style="text-align: center; padding: 20px; color: #666;">
        <p><strong>⚖️ ProVerBs Legal AI Platform</strong> | Version 1.0.0</p>
        <p>
            <a href="https://huggingface.co/Solomon7890" target="_blank">Hugging Face</a> | 
            <a href="https://github.com/Solomon7890" target="_blank">GitHub</a>
        </p>
        <p style="font-size: 0.9rem; margin-top: 10px;">
            ⚠️ <strong>Disclaimer</strong>: This AI provides general legal information only. 
            Consult with a licensed attorney for specific legal matters.
        </p>
        <p style="font-size: 0.85rem; color: #999;">
            © 2024 ProVerBs Legal AI. Built with ❤️ for legal professionals worldwide.
        </p>
    </div>
    """)

if __name__ == "__main__":
    demo.queue(max_size=20)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
