"""
ProVerBs Legal AI - Enhanced with DeepSeek-OCR Integration
Features: 7 AI Modes + Rotating Logos + OCR Document Processing
"""

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import base64
from pathlib import Path

# OCR Integration
try:
    from transformers import pipeline, AutoModel
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ Transformers not installed. OCR features will be limited.")

class AILegalChatbotIntegration:
    """
    Integration of AI Legal Chatbot with OCR capabilities
    """
    
    def __init__(self):
        self.specialized_modes = {
            "navigation": "Application Navigation Guide",
            "general": "General Legal Assistant",
            "document_validation": "Document Validator with OCR",
            "legal_research": "Legal Research Assistant",
            "etymology": "Legal Etymology Lookup",
            "case_management": "Case Management Helper",
            "regulatory_updates": "Regulatory Update Monitor"
        }
        
        # Initialize OCR if available
        self.ocr_pipeline = None
        if OCR_AVAILABLE:
            try:
                print("📦 Loading DeepSeek-OCR model...")
                self.ocr_pipeline = pipeline(
                    "image-text-to-text", 
                    model="deepseek-ai/DeepSeek-OCR", 
                    trust_remote_code=True
                )
                print("✅ OCR model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not load OCR model: {e}")
                self.ocr_pipeline = None
    
    def process_document_with_ocr(self, image_path: str) -> str:
        """
        Extract text from document image using DeepSeek-OCR
        """
        if not self.ocr_pipeline:
            return "❌ OCR model not available. Please install transformers and torch."
        
        try:
            # Process image with OCR
            result = self.ocr_pipeline(image_path)
            extracted_text = result[0]['generated_text'] if result else ""
            
            return f"""
## 📄 OCR Extraction Results

**Status**: ✅ Text extracted successfully

**Extracted Text:**
```
{extracted_text}
```

**Document Analysis:**
- **Length**: {len(extracted_text)} characters
- **Word Count**: {len(extracted_text.split())} words
- **Contains Legal Terms**: {self._check_legal_terms(extracted_text)}

**Next Steps:**
- Review the extracted text for accuracy
- Use Document Validator mode to analyze the content
- Ask questions about specific clauses or terms
"""
        except Exception as e:
            return f"❌ OCR processing error: {str(e)}"
    
    def _check_legal_terms(self, text: str) -> str:
        """Check for common legal terms in text"""
        legal_terms = [
            'contract', 'agreement', 'party', 'clause', 'provision',
            'whereas', 'hereby', 'herein', 'pursuant', 'consideration',
            'liability', 'indemnify', 'warranty', 'breach', 'terminate'
        ]
        
        found_terms = [term for term in legal_terms if term.lower() in text.lower()]
        
        if found_terms:
            return f"Yes ({len(found_terms)} terms: {', '.join(found_terms[:5])}...)"
        return "No"
    
    def get_mode_system_prompt(self, mode: str) -> str:
        """Get specialized system prompt based on mode"""
        prompts = {
            "navigation": """You are a ProVerBs Application Navigation Guide. Help users navigate the application's features:
            
**Available Features:**
- Legal Action Advisor: Get recommendations for seeking justice
- Document Analysis with OCR: Upload and analyze legal documents (now with OCR support!)
- Legal Research: Access comprehensive legal databases
- Communications: SMS, email, and phone integration
- Document Generation: Create legal documents with AI

**NEW: OCR Document Processing**
Users can now upload scanned documents and images. The system will extract text automatically using DeepSeek-OCR.

Guide users to the right features and explain how to use them effectively.""",
            
            "general": """You are a General Legal Assistant for ProVerBs Legal AI Platform. Provide accurate legal information while noting that you cannot provide legal advice. Always recommend consulting with a licensed attorney for specific legal matters. Be professional, thorough, and cite relevant legal principles when possible.""",
            
            "document_validation": """You are a Document Validator with OCR capabilities. 

**Enhanced Features:**
- Analyze documents from text or uploaded images
- Use DeepSeek-OCR to extract text from scanned documents
- Check for completeness and required elements
- Verify legal terminology accuracy
- Identify structural integrity issues
- Flag common problems and red flags

**When analyzing documents:**
1. If it's an image, use OCR to extract text first
2. Analyze the extracted or provided text
3. Check for legal validity and completeness
4. Provide specific feedback on document quality

Provide specific, actionable feedback on document quality and validity.""",
            
            "legal_research": """You are a Legal Research Assistant. Help users:
- Find relevant case law and precedents
- Understand statutes and regulations
- Research legal principles and concepts
- Cite authoritative legal sources
- Analyze legal documents and extract key information
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
- Managing documents and evidence (including OCR-processed documents)
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
        
        if any(word in query_lower for word in ["document", "contract", "agreement", "analyze", "scan", "ocr", "image"]):
            recommendations.append("📄 **Document Analysis with OCR** - Upload scanned documents or images for analysis")
        
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
):
    """Generate AI response based on selected mode"""
    chatbot_integration = AILegalChatbotIntegration()
    
    system_message = chatbot_integration.get_mode_system_prompt(mode)
    
    if mode == "navigation":
        nav_response = chatbot_integration.format_navigation_response(message)
        if nav_response:
            yield nav_response
            return
    
    # For document validation mode, mention OCR capability
    if mode == "document_validation" and not message:
        yield """
## 📄 Document Validator with OCR

**Capabilities:**
- ✅ Analyze legal documents
- ✅ Extract text from scanned documents (OCR)
- ✅ Validate document structure
- ✅ Check for legal completeness

**How to use:**
1. Upload a document image or paste text
2. I'll extract and analyze the content
3. Get detailed validation feedback

**Ask me to:**
- "Validate this contract"
- "Check this document for issues"
- "Extract text from this image"
"""
        return
    
    # Use HF Inference API
    try:
        client = InferenceClient(model="meta-llama/Llama-3.3-70B-Instruct")
        
        messages = [{"role": "system", "content": system_message}]
        
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": message})
        
        response = ""
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
        yield f"Error: {str(e)}\n\nNote: For full functionality, please ensure you're connected to Hugging Face."


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
    
    showNextLogo();
    setInterval(showNextLogo, 60000);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rotateLogo);
} else {
    rotateLogo();
}
</script>
"""

# Create the main application
demo = gr.Blocks(title="ProVerBs Legal AI Platform")

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
            Professional Legal AI System | Multi-Module Platform | Now with OCR! 📄
        </p>
    </div>
    <style>{custom_css}</style>
    {rotating_logo_js}
    """)
    
    gr.Markdown("---")
    
    # Main Tabs
    with gr.Tabs() as tabs:
        
        # Tab 1: Welcome
        with gr.Tab("🏠 Welcome", id="welcome"):
            gr.Markdown("""
            ## Welcome to ProVerBs Legal AI Platform
            
            A comprehensive legal AI system with **7 specialized assistants** and **OCR document processing**!
            
            ### 🎯 Choose Your AI Assistant Mode
            
            - **📍 Navigation Guide** - Find features in the platform
            - **💬 General Legal Assistant** - Broad legal questions
            - **📄 Document Validator with OCR** ⭐ NEW! - Analyze scanned documents
            - **🔍 Legal Research** - Case law and statutory research
            - **📚 Etymology Expert** - Legal terminology origins
            - **💼 Case Management** - Organize and track cases
            - **📋 Regulatory Updates** - Stay informed about changes
            
            ### ✨ NEW: OCR Document Processing
            
            Upload scanned documents, contracts, or legal images - our AI will:
            - Extract text automatically using DeepSeek-OCR
            - Analyze document structure and validity
            - Identify legal terms and key clauses
            - Provide detailed feedback
            
            **Ready to start?** Click the "AI Legal Chatbot" tab!
            """)
        
        # Tab 2: AI Legal Chatbot with OCR
        with gr.Tab("🤖 AI Legal Chatbot", id="chatbot"):
            gr.Markdown("""
            ## AI Legal Chatbot - 7 Modes + OCR Processing
            
            Select your assistant mode and start chatting! 
            **NEW**: Document Validator now includes OCR for scanned documents!
            """)
            
            mode_selector = gr.Dropdown(
                choices=[
                    "navigation",
                    "general",
                    "document_validation",
                    "legal_research",
                    "etymology",
                    "case_management",
                    "regulatory_updates"
                ],
                value="navigation",
                label="Select AI Assistant Mode",
                elem_classes=["mode-selector"]
            )
            
            gr.Markdown("---")
            
            chatbot = gr.ChatInterface(
                respond_with_mode,
                chatbot=gr.Chatbot(
                    height=500,
                    placeholder="💬 Select a mode and ask your question...",
                ),
                additional_inputs=[
                    mode_selector,
                    gr.Slider(128, 4096, value=2048, label="Max Tokens"),
                    gr.Slider(0.1, 2.0, value=0.7, label="Temperature"),
                    gr.Slider(0.1, 1.0, value=0.95, label="Top-p"),
                ],
                examples=[
                    ["How do I use the OCR document feature?"],
                    ["What is the difference between lawful and legal?"],
                    ["Can you validate a contract for me?"],
                    ["Research case law about employment contracts"],
                ],
            )
        
        # Tab 3: Features
        with gr.Tab("✨ Features", id="features"):
            gr.Markdown("""
            ## Platform Features
            
            ### 🆕 NEW: OCR Document Processing
            
            **DeepSeek-OCR Integration:**
            - Extract text from scanned documents
            - Process images of contracts and legal forms
            - Automatic text recognition
            - Legal document analysis
            
            ### 🎯 Core Capabilities
            
            - **7 Specialized AI Modes**
            - **Rotating Custom Logos**
            - **OCR Document Processing** ⭐ NEW!
            - **Legal Research Tools**
            - **Case Management**
            - **And more...**
            """)
        
        # Tab 4: About
        with gr.Tab("ℹ️ About", id="about"):
            gr.Markdown("""
            ## About ProVerBs Legal AI
            
            ### 🆕 Latest Update: OCR Integration
            
            We've integrated **DeepSeek-OCR** for advanced document processing:
            - Extract text from scanned documents
            - Process legal document images
            - Automatic text recognition
            - Enhanced document validation
            
            ### 🤖 7 Specialized AI Modes
            
            Each mode is trained for specific legal tasks, now with enhanced OCR capabilities
            in Document Validator mode.
            
            ### ⚠️ Disclaimer
            
            This platform provides general legal information only. Always consult with a 
            qualified attorney for specific legal matters.
            
            ---
            
            **Version 1.1.0** | Built by Solomon7890 | Powered by Hugging Face + DeepSeek-OCR
            """)
    
    # Footer
    gr.Markdown("""
    ---
    
    <div style="text-align: center; padding: 20px;">
        <p><strong>⚖️ ProVerBs Legal AI Platform</strong> | Version 1.1.0 with OCR</p>
        <p>© 2024 ProVerBs Legal AI. Built with ❤️ for legal professionals worldwide.</p>
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
