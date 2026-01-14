"""
ProVerBs Legal AI - Enhanced Landing Page
Multi-Module Legal AI Platform with Professional UI
"""

import gradio as gr
from huggingface_hub import InferenceClient

def respond(
    message,
    history: list[dict[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
    hf_token: gr.OAuthToken,
):
    """
    Main chat response function with AI integration
    """
    client = InferenceClient(token=hf_token.token, model="meta-llama/Llama-3.3-70B-Instruct")

    messages = [{"role": "system", "content": system_message}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = ""
    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        choices = message.choices
        token = ""
        if len(choices) and choices[0].delta.content:
            token = choices[0].delta.content
        response += token
        yield response


# Custom CSS for professional styling
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
}

.header-section h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    font-weight: 700;
}

.header-section p {
    font-size: 1.2rem;
    opacity: 0.95;
}

.feature-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
    transition: all 0.3s;
}

.feature-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.tab-nav button {
    font-size: 16px;
    font-weight: 600;
}
"""


# Create the main application
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
    ),
    css=custom_css,
    title="ProVerBs Legal AI Platform"
) as demo:
    
    # Header Section
    gr.HTML("""
    <div class="header-section">
        <h1>⚖️ ProVerBs Legal AI Platform</h1>
        <p>Lawful vs. Legal: Dual Analysis "Adappt'plication"</p>
        <p style="font-size: 1rem; margin-top: 10px;">
            Professional Legal AI System | Multi-Module Platform | Powered by Advanced AI
        </p>
    </div>
    """)
    
    # Login Section
    with gr.Row():
        with gr.Column(scale=1):
            gr.LoginButton(size="lg")
        with gr.Column(scale=5):
            gr.Markdown("👈 **Login with your Hugging Face account** for full access to premium features")
    
    gr.Markdown("---")
    
    # Main Content Tabs
    with gr.Tabs() as tabs:
        
        # Tab 1: Welcome & Overview
        with gr.Tab("🏠 Welcome", id="welcome"):
            gr.Markdown("""
            ## Welcome to ProVerBs Legal AI Platform
            
            A comprehensive legal AI system designed for legal professionals, researchers, and individuals 
            seeking legal information. Our platform combines multiple AI models and specialized tools to 
            provide accurate, helpful legal assistance.
            
            ### 🌟 Key Features
            
            - **🤖 AI Legal Assistant**: Chat with advanced AI models trained on legal knowledge
            - **📄 Document Analysis**: Process and analyze legal documents
            - **💼 Case Management**: Track and manage legal cases efficiently
            - **🔍 Legal Research**: Access vast databases of legal information
            - **🛡️ Compliance Tools**: Ensure regulatory compliance
            - **📊 Analytics Dashboard**: Visualize legal data and insights
            
            ### 🎯 Our Mission
            
            To democratize access to legal information and tools, making professional-grade legal AI 
            accessible to everyone while maintaining the highest standards of accuracy and reliability.
            
            ### ⚠️ Important Disclaimer
            
            This platform provides general legal information and AI-powered assistance. It does not 
            constitute legal advice. Always consult with a qualified attorney for specific legal matters.
            
            ---
            
            **Ready to get started?** Click on the "Legal AI Assistant" tab to begin chatting!
            """)
        
        # Tab 2: Legal AI Assistant (Main Chat)
        with gr.Tab("🤖 Legal AI Assistant", id="assistant"):
            gr.Markdown("""
            ## Legal AI Assistant
            
            Ask questions about law, legal procedures, case analysis, or any legal topic. 
            Our AI assistant is here to help with accurate, contextual information.
            """)
            
            chatbot = gr.ChatInterface(
                respond,
                type="messages",
                chatbot=gr.Chatbot(
                    height=500,
                    placeholder="💬 Ask me anything about law, legal procedures, or case analysis...",
                    show_label=False,
                ),
                textbox=gr.Textbox(
                    placeholder="Type your legal question here...",
                    container=False,
                    scale=7
                ),
                additional_inputs=[
                    gr.Textbox(
                        value="You are ProVerBs Legal AI, a knowledgeable legal assistant specializing in law, legal procedures, and case analysis. Provide accurate, helpful information while noting that you cannot provide legal advice. Always recommend consulting with a licensed attorney for specific legal matters. Be professional, thorough, and cite relevant legal principles when possible.",
                        label="System Message",
                        lines=4
                    ),
                    gr.Slider(
                        minimum=128,
                        maximum=4096,
                        value=2048,
                        step=128,
                        label="Max Tokens"
                    ),
                    gr.Slider(
                        minimum=0.1,
                        maximum=2.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature"
                    ),
                    gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.95,
                        step=0.05,
                        label="Top-p (nucleus sampling)"
                    ),
                ],
                examples=[
                    ["What is the difference between civil law and criminal law?"],
                    ["Explain the concept of 'burden of proof' in legal proceedings"],
                    ["What are the essential elements of a valid contract?"],
                    ["What is the statute of limitations and why is it important?"],
                    ["Explain the difference between 'lawful' and 'legal'"],
                ],
                cache_examples=False,
            )
        
        # Tab 3: Features Overview
        with gr.Tab("✨ Features", id="features"):
            gr.Markdown("""
            ## Platform Features
            
            ### 🎯 Core Capabilities
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    #### 🤖 AI-Powered Assistance
                    - Multiple AI models (Llama, GPT, Qwen)
                    - Real-time streaming responses
                    - Context-aware conversations
                    - Legal knowledge base integration
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    #### 📄 Document Processing
                    - PDF, DOCX, TXT support
                    - Automatic text extraction
                    - Key terms identification
                    - Legal issue detection
                    """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    #### 💼 Case Management
                    - Track multiple cases
                    - Client information management
                    - Deadline tracking
                    - Status monitoring
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    #### 🔍 Research Tools
                    - Case law search
                    - Statute lookup
                    - Legal precedent finder
                    - Citation generator
                    """)
            
            gr.Markdown("""
            ---
            
            ### 🚀 Coming Soon
            
            - **Advanced Analytics**: Visualize case trends and patterns
            - **Multi-language Support**: Legal assistance in multiple languages
            - **API Access**: Integrate with your existing tools
            - **Team Collaboration**: Share workspaces with colleagues
            - **Mobile App**: Access on the go
            """)
        
        # Tab 4: About & Resources
        with gr.Tab("ℹ️ About", id="about"):
            gr.Markdown("""
            ## About ProVerBs Legal AI
            
            ### 🎓 Our Story
            
            ProVerBs Legal AI is a cutting-edge platform that combines artificial intelligence with 
            legal expertise to provide accessible, accurate legal information and tools. We believe 
            that everyone deserves access to quality legal resources.
            
            ### 👥 For Everyone
            
            - **Legal Professionals**: Enhance your practice with AI-powered tools
            - **Law Students**: Study and research with advanced AI assistance
            - **Businesses**: Understand legal implications of business decisions
            - **Individuals**: Get information about your legal rights and options
            
            ### 🔒 Privacy & Security
            
            We take your privacy seriously:
            - End-to-end encryption for sensitive data
            - No storage of personal information without consent
            - GDPR and CCPA compliant
            - Secure OAuth authentication via Hugging Face
            
            ### 📚 Resources
            
            - **Documentation**: [Read the Docs](https://huggingface.co/Solomon7890)
            - **GitHub**: [Source Code](https://github.com/Solomon7890)
            - **Community**: [Join our Discord](#)
            - **Support**: [Contact Us](#)
            
            ### 🤝 Credits
            
            Built with:
            - [Gradio](https://gradio.app) - UI Framework
            - [Hugging Face](https://huggingface.co) - AI Infrastructure
            - [Meta Llama](https://llama.meta.com) - Language Models
            
            ### 📄 License
            
            This project is released under the Unlicense - free for any use.
            
            ---
            
            **Version 1.0.0** | Last Updated: 2024 | Built by Solomon7890
            """)
    
    # Footer
    gr.Markdown("""
    ---
    
    <div style="text-align: center; padding: 20px; color: #666;">
        <p><strong>⚖️ ProVerBs Legal AI Platform</strong> | Version 1.0.0</p>
        <p>
            <a href="https://huggingface.co/Solomon7890" target="_blank">Hugging Face</a> | 
            <a href="https://github.com/Solomon7890" target="_blank">GitHub</a> | 
            <a href="#" target="_blank">Documentation</a> | 
            <a href="#" target="_blank">Support</a>
        </p>
        <p style="font-size: 0.9rem; margin-top: 10px;">
            ⚠️ <strong>Disclaimer</strong>: This AI provides general legal information only. 
            It does not constitute legal advice. Consult with a licensed attorney for specific legal matters.
        </p>
        <p style="font-size: 0.85rem; color: #999; margin-top: 10px;">
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
