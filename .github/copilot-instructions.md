# ShortListResumes - AI Coding Instructions

## Project Overview
ShortListResumes is a Python resume screening application using a **multi-agent pipeline architecture**. Each agent handles a specific task in sequence: filtering → scoring → rating → feedback generation.

## Core Architecture

### Agent-Based Pipeline Pattern
- **Framework**: Custom agent base class (imported from `base_agent.BaseAgent` in [src/agents/__init__.py](../../src/agents/__init__.py))
- **Primary Flow**: `FilterAgent` → `ScoringAgent` → `RateAgent` (linear pipeline)
- **Feedback Loop**: `FeedbackAgent` is a **loopAgent** (iterative loop) and **sequentialAgent** that iteratively calls `FilterAgent` until finding perfect matches
  - Loops with tightening/refined criteria each iteration
  - Sequential execution: refines search criteria one at a time
  - Returns top candidates that meet enhanced quality thresholds
- **Data model**: Resumes flow through agents as `Resume` objects ([src/agents/filter_agent.py](../../src/agents/filter_agent.py#L6-L14)), transformed into intermediate results (`ScoreResult` in [src/agents/scoring_agent.py](../../src/agents/scoring_agent.py#L16-L19))

### Key Components

**FilterAgent** ([src/agents/filter_agent.py](../../src/agents/filter_agent.py))
- Filters resumes by job keywords and experience requirements
- **Critical pattern**: Protected attribute checking - rejects filters on `gender`, `race`, `religion`, `age`, `sexual_orientation` with warnings
- Applies safe biases: `location`, `required_skill`

**ScoringAgent** ([src/agents/scoring_agent.py](../../src/agents/scoring_agent.py))
- Multi-method scoring: heuristic keyword matching + optional Vertex AI LLM augmentation
- Domain detection via `DOMAIN_KEYWORDS` lookup dictionary
- Supports optional external LinkedIn validation callback
- **Integration point**: Optional Google Vertex AI for enhanced analysis (pass `vertex_model_name` to enable)

**RateAgent** ([src/agents/rate_agent.py](../../src/agents/rate_agent.py))
- Converts scores to rankings (1 = top candidate)

**FeedbackAgent** ([src/agents/feedback_agent.py](../../src/agents/feedback_agent.py)) - LoopAgent Pattern
- **Type**: Iterative loopAgent and sequentialAgent that searches for perfect matches
- Calls `FilterAgent` iteratively with progressively refined/tightened criteria
- Loops until finding candidates that meet quality thresholds (perfect match conditions)
- Sequential execution: refines one criterion at a time across iterations
- Generates human-readable feedback summaries for matched candidates

## Data Structures & Conventions

### Resume Model
```python
Resume(
    id: str,                    # unique identifier
    full_name: str,
    text: str,                  # resume content
    experience: List[str],      # job roles/companies
    metadata: Dict,             # years_experience, location, etc.
    email: str = "",
    linkedin_url: str = ""
)
```

### Job Description Format
```python
job_desc = {
    "keywords": List[str],              # skill/role keywords to match
    "min_years_experience": int
}
```

### Biases Parameter (Filtering)
```python
biases = {
    "location": str,                    # geographic filter (allowed)
    "required_skill": str,              # skill filter (allowed)
    # NOTE: gender, race, religion, age, sexual_orientation cause warnings and are ignored
}
```

## Development Workflows

**Run the pipeline**:
```bash
python src/main.py
```

**Run tests**:
```bash
pytest tests/
```

**Environment setup**: Create `.env` file (see `.env.example`) for `DATABASE_URL`, `LOG_LEVEL`, `MAX_RESUMES`

## Project-Specific Patterns

1. **Agent initialization**: All agents implement `initialize()` method (currently returns `None` but reserved for future setup)

2. **Scoring heuristic**: [ScoringAgent.score()](../../src/agents/scoring_agent.py#L107-L135)
   - Base score: 100.0
   - Deductions: LinkedIn found (-10), each domain found (-5), years of experience (×0.5)
   - Results sorted ascending (lower score = better match)

3. **Domain detection**: Hardcoded keyword map for `finance`, `healthcare`, `ml`, `web` domains in [DOMAIN_KEYWORDS](../../src/agents/scoring_agent.py#L9-L13)

4. **Warning system**: FilterAgent collects warnings about protected attribute filters; access via `agent.warnings` list

## External Dependencies & Integration

- **Flask** (2.0.1): Web framework (present in requirements but not yet integrated in main pipeline)
- **python-dotenv**: Environment variable loading via [src/config/settings.py](../../src/config/settings.py)
- **Google Vertex AI**: Optional LLM integration for enhanced resume analysis (gracefully disabled if unavailable)
- **pytest**: Testing framework

## Important Notes for AI Agents

- **Missing implementations**: `BaseAgent` class and `ShortlisterAgent` are imported but not yet in codebase (references in test suggest upcoming implementation)
- **Score interpretation**: Lower scores = better candidates (counterintuitive but confirmed in [RateAgent](../../src/agents/rate_agent.py#L9))
- **Error handling**: Most agents use try-except to gracefully degrade (e.g., Vertex AI failures don't block scoring)
- **Threading/Async**: None currently - pipeline is sequential and synchronous
