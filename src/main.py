from agents.filter_agent import Resume, FilterAgent
from agents.scoring_agent import ScoringAgent
from agents.rate_agent import RateAgent
from agents.feedback_agent import FeedbackAgent
from agents.shortlister_agent import ShortlisterAgent

def example_external_link_check(name: str) -> bool:
    # placeholder; implement real HTTP lookup if desired
    return "linkedin" in name.lower()

def main():
    resumes = [
        Resume(id="r1", full_name="Alice Johnson", text="Experienced ML engineer with deep learning and NLP", linkedin_url="", experience=["Google - ML"], metadata={"years_experience": 6, "location": "NY"}),
        Resume(id="r2", full_name="Bob Smith", text="Senior backend engineer, Django, Flask, web services", linkedin_url="https://linkedin.example/bob", experience=["Startup - Backend"], metadata={"years_experience": 8, "location": "SF"}),
        Resume(id="r3", full_name="Cara Lee", text="Finance analyst, accounting and trading systems", linkedin_url="", experience=["Bank - Finance"], metadata={"years_experience": 4, "location": "NY"}),
    ]

    job_desc = {"keywords": ["engineer", "ml"], "min_years_experience": 3}
    biases = {"gender": "female", "location": "NY", "required_skill": "ml"}

    f = FilterAgent()
    filtered = f.filter(resumes, job_desc, biases)
    s = ScoringAgent(external_link_check=example_external_link_check)
    scored = s.score(filtered)
    r = RateAgent()
    rated = r.rate(scored)
    fb = FeedbackAgent()
    feedback = fb.feedback_for(scored, top_n=1)

    print("Warnings:", f.warnings)
    print("Rated:", rated)
    print("Feedback:")
    for line in feedback:
        print("-", line)

    # Initialize the ShortlisterAgent
    agent = ShortlisterAgent()
    agent.initialize()

    # Execute the agent's functionality
    agent.execute()

if __name__ == "__main__":
    main()