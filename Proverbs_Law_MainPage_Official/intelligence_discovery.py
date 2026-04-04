from huggingface_hub import HfApi
import json
import os
from firecrawl_scout import UniversalScoutEngine

class ModelDiscoveryEngine:
    def __init__(self):
        self.api = HfApi()
        self.scout = UniversalScoutEngine()
        self.config_path = "dynamic_models.json"
        
    def discover_latest_legal_models(self) -> dict:
        """
        Queries HuggingFace for top 5 legal models by likes.
        """
        try:
            # 1. Scout the Global Legal Tech Web (Deep Discovery)
            print("🌊 Engaged Global Firecrawl Scout for Legal AI Breakthroughs...")
            scout_news = self.scout.scout_legal_domain("https://huggingface.co/blog?tag=legal")
            
            # 2. Query the hub for legal domain models
            models = self.api.list_models(
                filter="legal",
                sort="likes",
                direction=-1,
                limit=5
            )
            
            discovered = []
            for m in models:
                discovered.append({
                    "id": m.id,
                    "likes": getattr(m, 'likes', 0),
                    "tags": m.tags if hasattr(m, 'tags') else [],
                    "last_modified": m.last_modified if hasattr(m, 'last_modified') else "unknown"
                })
                
            intelligence_report = {
                "discovered": discovered,
                "timestamp": str(os.path.getmtime(self.config_path)) if os.path.exists(self.config_path) else "0",
                "source": "HuggingFace Hub"
            }
            
            # Save local copy
            with open(self.config_path, "w") as f:
                json.dump(intelligence_report, f, indent=4)
                
            return intelligence_report
            
        except Exception as e:
            print(f"❌ Discovery Intelligence error: {str(e)}")
            return {"error": str(e)}

if __name__ == "__main__":
    discovery = ModelDiscoveryEngine()
    print(json.dumps(discovery.discover_latest_legal_models(), indent=2))
