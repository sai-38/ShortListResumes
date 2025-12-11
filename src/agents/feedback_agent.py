from typing import List
from .scoring_agent import ScoreResult
from .base_agent import BaseAgent

class FeedbackAgent(BaseAgent):
    def initialize(self):
        return None

    def feedback_for(self, scored: List[ScoreResult], top_n: int = 1) -> List[str]:
        """
        Returns simple feedback strings per resume. Starts by giving feedback for top profiles first.
        """
        lines: List[str] = []
        for idx, s in enumerate(scored, start=1):
            tag = f"Top {idx}" if idx <= top_n else f"#{idx}"
            domains = ", ".join(s.domains) if s.domains else "general"
            linkedin = "has LinkedIn" if s.linkedin_found else "no LinkedIn found"
            lines.append(f"{tag} - {s.resume.full_name}: strong in {domains}; {linkedin}.")
        return lines