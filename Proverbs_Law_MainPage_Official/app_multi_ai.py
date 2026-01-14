"""
ProVerBs Legal AI - Multi-AI Model Integration
Supports: GPT-4, Gemini, Perplexity, NinjaAI, LM Studio, and HuggingFace models
"""

import gradio as gr
from huggingface_hub import InferenceClient
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests

class MultiAIProvider:
    """
    Multi-AI provider supporting multiple models
    """
    
    def __init__(self):
        self.providers = {
            "huggingface": "Llama-3.3-70B (HuggingFace)",
            "gpt4": "GPT-4 (OpenAI)",
            "gemini": "Gemini 3.0 (Google)",
            "perplexity": "Perplexity AI",
            "ninjaai": "Ninja AI",
            "lmstudio": "LM Studio (Local)"
        }
        
        # API endpoints
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
            yield "⚠️ OpenAI API key not set. Please set OPENAI_API_KEY environment variable."
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
            response = requests.post(
                self.endpoints["gpt4"],
                headers=headers,
                json=data,
                stream=True
            )
            
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
            yield "⚠️ Google API key not set. Please set GOOGLE_API_KEY environment variable."
            return
        
        # Convert messages to Gemini format
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
            yield "⚠️ Perplexity API key not set. Please set PERPLEXITY_API_KEY environment variable."
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
            response = requests.post(
                self.endpoints["perplexity"],
                headers=headers,
                json=data,
                stream=True
            )
            
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
            yield "⚠️ NinjaAI API key not set. Please set NINJAAI_API_KEY environment variable."
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
            response = requests.post(
                self.endpoints["ninjaai"],
                headers=headers,
                json=data,
                stream=True
            )
            
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
            response = requests.post(
                self.endpoints["lmstudio"],
                headers=headers,
                json=data,
                stream=True,
                timeout=5
            )
            
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
            yield "⚠️ LM Studio not running. Please start LM Studio server on localhost:1234"
        except Exception as e:
            yield f"❌ LM Studio Error: {str(e)}"
    
    def call_huggingface(self, messages: List[Dict], max_tokens: int, temperature: float, top_p: float, hf_token=None):
        """Call HuggingFace Inference API"""
        token = hf_token.token if hf_token else None
        client = InferenceClient(token=token, model="meta-llama/Llama-3.3-70B-Instruct")
        
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
    """
    Integration of AI Legal Chatbot with Multi-AI support
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
- Audio Analysis: Process audio with Supertonic AI

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
        
        if any(word in query_lower for word in ["audio", "voice", "sound", "recording"]):
            recommendations.append("🎵 **Audio Analysis** - Process audio with Supertonic AI")
        
        if recommendations:
            return "### I can help you with these features:\n\n" + "\n".join(recommendations) + "\n\n**What would you like to explore?**"
        
        return None
