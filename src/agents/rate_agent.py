from typing import List
from .scoring_agent import ScoreResult
from .base_agent import BaseAgent

class RateAgent(BaseAgent):
    def initialize(self):
        return None

    def rate(self, scored: List[ScoreResult]) -> List[dict]:
        """
        Accepts scored results sorted with best (lowest score) first.
        Returns list of dicts with rating where 1 is top.
        """
        out: List[dict] = []
        for idx, s in enumerate(scored, start=1):
            out.append({
                "id": s.resume.id,
                "full_name": s.resume.full_name,
                "rating": idx,   # 1 is top
                "linkedin_found": s.linkedin_found,
                "domains": s.domains,
                "raw_score": s.score
            })
        return out