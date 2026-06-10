import json
import re
from datetime import datetime

class AnalystAgent:
    """
    Interpretation Agent grounded in 'Agents in Trustworthy' (Section 2.1.2).
    Uses a weighted lexicon to calculate confidence scores for discovered articles.
    """
    
    LEXICON = {
        "Legal": {
            "weight": 2.0,
            "terms": ["lawsuit", "appeal", "indictment", "grand jury", "docket", "litigation", 
                      "probate", "guardianship", "bench warrant", "judge", "court", "attorney"]
        },
        "Political": {
            "weight": 1.5,
            "terms": ["election", "political", "city council", "commissioners court", 
                      "public hearing", "bond election", "canvass", "charter amendment", "precinct"]
        },
        "Regional": {
            "weight": 1.0,
            "terms": ["killeen", "central texas", "bell county", "temple", "fort cavazos", 
                      "harker heights", "copperas cove", "nolanville", "belton"]
        }
    }

    def __init__(self):
        pass

    def rank_article(self, article):
        """
        Calculates a confidence score and provides reasoning (Section 8.4).
        """
        text = f"{article.get('title', '')} {article.get('content', '')}".lower()
        scores = {}
        matches = {}

        total_score = 0
        for category, data in self.LEXICON.items():
            cat_matches = []
            cat_score = 0
            for term in data["terms"]:
                count = len(re.findall(r'\b' + re.escape(term) + r'\b', text))
                if count > 0:
                    cat_score += count * data["weight"]
                    cat_matches.append(f"{term} ({count})")
            
            if cat_score > 0:
                scores[category] = cat_score
                matches[category] = cat_matches
                total_score += cat_score

        # Confidence level calculation (normalized or raw)
        # For 'Simpler-First', we'll use raw score but flag high confidence
        confidence_level = "High" if total_score > 10 else "Medium" if total_score > 3 else "Low"

        reasoning = f"Confidence {confidence_level} based on: "
        reasoning += "; ".join([f"{cat}: {', '.join(m)}" for cat, m in matches.items()])

        return {
            "confidence_score": round(total_score, 2),
            "confidence_level": confidence_level,
            "reasoning": reasoning,
            "analyzed_at": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Quick test
    analyst = AnalystAgent()
    test_article = {
        "title": "Killeen City Council to discuss new lawsuit and election procedures",
        "content": "The judge oversaw the appeal regarding the Central Texas redistricting."
    }
    result = analyst.rank_article(test_article)
    print(json.dumps(result, indent=2))
