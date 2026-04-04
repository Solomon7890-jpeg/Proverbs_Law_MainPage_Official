import os
from firecrawl import FirecrawlApp
from typing import List, Dict, Optional
import json

class UniversalScoutEngine:
    """
    The 'Sensory Layer' for the ProVerBs Legal AI.
    Uses Firecrawl to map and crawl live legal/technical domains.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            print("⚠️ FIRECRAWL_API_KEY not found. Scout operating in offline mode.")
            self.app = None
        else:
            self.app = FirecrawlApp(api_key=self.api_key)

    def scout_legal_domain(self, domain_url: str, depth: int = 2) -> Dict:
        """
        Maps a legal domain and crawls key content into LLM-ready markdown.
        """
        if not self.app:
            return {"error": "API key required for live scouting."}

        try:
            print(f"📡 Scouting {domain_url} (Depth: {depth})...")
            # 1. Map the domain to identify relevant statutes/pages
            map_result = self.app.map_url(domain_url)
            
            # 2. Crawl the top relevant pages (limit to top 5 for efficiency)
            top_links = map_result.get('links', [])[:5]
            crawl_data = []
            
            for link in top_links:
                page_data = self.app.scrape_url(link, params={'formats': ['markdown']})
                crawl_data.append(page_data)
                
            intelligence_packet = {
                "source": domain_url,
                "map": map_result,
                "crawled_content": crawl_data,
                "status": "success"
            }
            
            # Save for the Brain to reference
            with open("scout_intelligence_packet.json", "w") as f:
                json.dump(intelligence_packet, f, indent=4)
                
            return intelligence_packet
            
        except Exception as e:
            print(f"❌ Scouting Error: {str(e)}")
            return {"error": str(e)}

    def aesthetic_scout(self) -> List[str]:
        """
        Crawl luxury corporate design sites for current 'Optimal Quality' aesthetics.
        Returns a list of premium design tokens (colors, styles).
        """
        # Example premium design sources
        sources = ["https://www.awwwards.com/websites/corporate/"]
        # Simplified implementation for now
        return ["#09090b", "#eab308", "glassmorphism", "3D particles"]

if __name__ == "__main__":
    scout = UniversalScoutEngine()
    # Test with a high-level legal portal (if key provided)
    # scout.scout_legal_domain("https://www.law.cornell.edu/wex")
