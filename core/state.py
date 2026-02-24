from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ResearchState:
    query: str
    sub_questions: List[str] = None
    research_plan: str = ''
    findings: List[Dict[str, Any]] = None
    contradictions: List[str] = None
    credibility_scores: List[Dict[str, float]] = None
    synthesis: str = ''
    confidence: float = 0.0
    sources: List[str] = None
    thinking_log: List[str] = None

    def __post_init__(self):
        if self.sub_questions is None:
            self.sub_questions = []
        if self.findings is None:
            self.findings = []
        if self.contradictions is None:
            self.contradictions = []
        if self.credibility_scores is None:
            self.credibility_scores = []
        if self.sources is None:
            self.sources = []
        if self.thinking_log is None:
            self.thinking_log = []
