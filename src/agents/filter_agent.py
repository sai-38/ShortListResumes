from dataclasses import dataclass, field
from typing import List, Dict, Any, Iterable
from .base_agent import BaseAgent

PROTECTED_ATTRIBUTES = {"gender", "race", "religion", "age", "sexual_orientation"}

@dataclass
class Resume:
    id: str
    full_name: str
    text: str
    email: str = ""
    linkedin_url: str = ""
    experience: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class FilterAgent(BaseAgent):
    def __init__(self):
        self.warnings: List[str] = []

    def initialize(self):
        return None

    def _check_biases(self, biases: Dict[str, Any]) -> Dict[str, Any]:
        safe_biases: Dict[str, Any] = {}
        for k, v in (biases or {}).items():
            if k.lower() in PROTECTED_ATTRIBUTES:
                self.warnings.append(f"Ignored protected attribute filter: {k}")
                continue
            safe_biases[k] = v
        return safe_biases

    def filter(self, resumes: Iterable[Resume], job_desc: Dict[str, Any], biases: Dict[str, Any] = None) -> List[Resume]:
        biases = biases or {}
        safe_biases = self._check_biases(biases)
        results: List[Resume] = []
        keywords = set((job_desc.get("keywords") or []))
        min_years = job_desc.get("min_years_experience", 0)

        for r in resumes:
            text_lower = (r.text or "").lower()
            # keyword matching
            if keywords:
                if not any(kw.lower() in text_lower for kw in keywords):
                    continue
            # simple experience check via metadata years_experience
            years = r.metadata.get("years_experience", 0)
            if years < min_years:
                continue
            # apply simple allowed bias filters (e.g., location, required_skill)
            ok = True
            for k, v in safe_biases.items():
                if k == "location":
                    if v.lower() not in (r.metadata.get("location","").lower()):
                        ok = False
                        break
                if k == "required_skill":
                    if v.lower() not in text_lower:
                        ok = False
                        break
            if ok:
                results.append(r)
        return results