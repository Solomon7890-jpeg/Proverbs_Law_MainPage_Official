"""
Analytics & SEO Module for ProVerBs Ultimate Brain
- Google Analytics integration
- Query tracking
- User behavior analytics
- SEO optimization
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AnalyticsTracker:
    """Track user queries and interactions"""
    
    def __init__(self):
        self.queries: List[Dict] = []
        self.sessions: Dict[str, Dict] = {}
        self.popular_modes: Dict[str, int] = {}
        self.popular_ai_models: Dict[str, int] = {}
    
    def track_query(
        self,
        query: str,
        mode: str,
        ai_provider: str,
        reasoning_enabled: bool,
        response_time: float,
        success: bool
    ):
        """Track a query"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query[:100],  # Truncate for privacy
            "mode": mode,
            "ai_provider": ai_provider,
            "reasoning_enabled": reasoning_enabled,
            "response_time": response_time,
            "success": success
        }
        
        self.queries.append(entry)
        
        # Track mode popularity
        self.popular_modes[mode] = self.popular_modes.get(mode, 0) + 1
        
        # Track AI model popularity
        self.popular_ai_models[ai_provider] = self.popular_ai_models.get(ai_provider, 0) + 1
        
        logger.info(f"Tracked query: {query[:50]}... [Mode: {mode}, AI: {ai_provider}]")
    
    def get_analytics(self) -> Dict:
        """Get analytics summary"""
        total_queries = len(self.queries)
        successful_queries = sum(1 for q in self.queries if q['success'])
        avg_response_time = sum(q['response_time'] for q in self.queries) / total_queries if total_queries > 0 else 0
        
        # Get top modes
        top_modes = sorted(self.popular_modes.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Get top AI models
        top_ai = sorted(self.popular_ai_models.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "success_rate": f"{(successful_queries/total_queries*100):.2f}%" if total_queries > 0 else "0%",
            "avg_response_time": f"{avg_response_time:.2f}s",
            "top_modes": top_modes,
            "top_ai_models": top_ai,
            "queries_with_reasoning": sum(1 for q in self.queries if q['reasoning_enabled']),
            "recent_queries": self.queries[-10:][::-1]  # Last 10, reversed
        }
    
    def export_analytics(self, filepath: str = "analytics_data.json"):
        """Export analytics to JSON file"""
        data = self.get_analytics()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Analytics exported to {filepath}")


class SEOOptimizer:
    """SEO optimization utilities"""
    
    @staticmethod
    def get_meta_tags() -> str:
        """Generate SEO meta tags"""
        return """
        <meta name="description" content="ProVerBs Ultimate Legal AI Brain - Advanced legal assistant with 100+ reasoning protocols, multi-AI support, and specialized legal modes. Free to use.">
        <meta name="keywords" content="legal AI, legal assistant, chain of thought, reasoning AI, legal research, document validation, ProVerBs, ADAPPT-I, quantum reasoning">
        <meta name="author" content="Solomon7890">
        <meta name="robots" content="index, follow">
        <meta property="og:title" content="ProVerBs Ultimate Legal AI Brain">
        <meta property="og:description" content="The most advanced legal AI platform with 100+ reasoning protocols and multi-AI support">
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE">
        <meta property="og:image" content="https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE/resolve/main/preview.png">
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="ProVerBs Ultimate Legal AI Brain">
        <meta name="twitter:description" content="Advanced legal AI with 100+ reasoning protocols">
        """
    
    @staticmethod
    def get_structured_data() -> str:
        """Generate JSON-LD structured data for SEO"""
        return """
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "SoftwareApplication",
          "name": "ProVerBs Ultimate Legal AI Brain",
          "description": "Advanced legal AI assistant with 100+ reasoning protocols, multi-AI support, and specialized legal modes",
          "applicationCategory": "LegalTechnology",
          "operatingSystem": "Web Browser",
          "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
          },
          "author": {
            "@type": "Person",
            "name": "Solomon7890"
          },
          "featureList": [
            "100+ Reasoning Protocols",
            "6 AI Models (GPT-4, Gemini, Perplexity, etc.)",
            "7 Specialized Legal Modes",
            "Chain-of-Thought Reasoning",
            "Document Validation",
            "Legal Research Assistant"
          ]
        }
        </script>
        """


# Global analytics tracker
analytics_tracker = AnalyticsTracker()
