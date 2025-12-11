from typing import Iterable, List, Callable, Optional
from dataclasses import dataclass
from .filter_agent import Resume
from .base_agent import BaseAgent
import json

DOMAIN_KEYWORDS = {
    "finance": ["finance", "bank", "trading", "accounting"],
    "healthcare": ["health", "clinical", "hospital", "patient"],
    "ml": ["machine learning", "deep learning", "nlp", "computer vision"],
    "web": ["javascript", "react", "frontend", "backend", "django", "flask"]
}

@dataclass
class ScoreResult:
    resume: Resume
    linkedin_found: bool
    domains: List[str]
    score: float

class ScoringAgent(BaseAgent):
    def __init__(
        self,
        external_link_check: Callable[[str], bool] = None,
        vertex_model_name: Optional[str] = None,
        vertex_project: Optional[str] = None,
        vertex_location: Optional[str] = "us-central1",
    ):
        """
        external_link_check: optional function that accepts full_name or url and returns bool indicating LinkedIn presence.
        vertex_model_name: optional Vertex AI text generation model id (e.g. "text-bison@001") to assist detection.
        vertex_project/vertex_location: used to init Vertex AI SDK if vertex_model_name provided.
        """
        self.external_link_check = external_link_check
        self.vertex_model_name = vertex_model_name
        self.vertex_project = vertex_project
        self.vertex_location = vertex_location
        self.vertex_model = None
        if self.vertex_model_name:
            self._init_vertex_model()

    def initialize(self):
        return None

    def _init_vertex_model(self):
        try:
            import google.cloud.aiplatform as aiplatform  # type: ignore
            aiplatform.init(project=self.vertex_project, location=self.vertex_location)
            # Use TextGenerationModel API when available
            try:
                self.vertex_model = aiplatform.TextGenerationModel.from_pretrained(self.vertex_model_name)
            except Exception:
                # fallback: try Model with endpoint predict — keep None if unavailable
                self.vertex_model = None
        except Exception:
            self.vertex_model = None

    def _detect_domains(self, text: str):
        text_l = (text or "").lower()
        found: List[str] = []
        for domain, kws in DOMAIN_KEYWORDS.items():
            if any(k in text_l for k in kws):
                found.append(domain)
        return found

    def _vertex_analyze(self, text: str) -> dict:
        if not self.vertex_model:
            return {}
        prompt = (
            "Analyze the resume text below and return a JSON object with keys:\n"
            "  linkedin_found: true/false\n"
            "  domains: list of short domain strings (e.g. ml, web, finance)\n\n"
            "Respond ONLY with valid JSON.\n\n"
            f"Resume:\n{text}\n"
        )
        try:
            resp = self.vertex_model.predict(prompt, max_output_tokens=256, temperature=0)
            # resp may be a string or object with .text() depending on SDK version
            out_text = str(resp)
            # try to extract JSON object from the output
            start = out_text.find("{")
            end = out_text.rfind("}") + 1
            if start != -1 and end != -1:
                candidate = out_text[start:end]
                return json.loads(candidate)
        except Exception:
            pass
        return {}

    def score(self, resumes: Iterable[Resume]) -> List[ScoreResult]:
        results: List[ScoreResult] = []
        for r in resumes:
            linkedin_found = False
            if r.linkedin_url:
                linkedin_found = True
            elif self.external_link_check:
                try:
                    linkedin_found = bool(self.external_link_check(r.full_name))
                except Exception:
                    linkedin_found = False

            # try Vertex AI to enhance detection if available
            vertex_info = {}
            if self.vertex_model:
                try:
                    vertex_info = self._vertex_analyze(r.text + " " + " ".join(r.experience))
                    if isinstance(vertex_info.get("linkedin_found"), bool):
                        linkedin_found = vertex_info.get("linkedin_found")
                except Exception:
                    vertex_info = {}

            # domains: combine heuristic and vertex result if present
            domains = self._detect_domains(r.text + " " + " ".join(r.experience))
            if vertex_info.get("domains"):
                try:
                    vdoms = list(dict.fromkeys([d.lower() for d in vertex_info.get("domains")]))
                    # merge preserving uniqueness
                    for d in vdoms:
                        if d not in domains:
                            domains.append(d)
                except Exception:
                    pass

            years = r.metadata.get("years_experience", 0)
            score = 100.0
            score -= (10 if linkedin_found else 0)
            score -= (5 * len(domains))
            score -= min(years, 20) * 0.5
            results.append(ScoreResult(resume=r, linkedin_found=linkedin_found, domains=domains, score=score))
        return sorted(results, key=lambda s: s.score)