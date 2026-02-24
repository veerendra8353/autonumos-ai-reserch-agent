import os
from dotenv import load_dotenv
load_dotenv()

from core.build_graph import build_graph
from core.state import ResearchState

def run(query: str) -> ResearchState:
    graph = build_graph()
    initial_state = ResearchState(
        query=query,
        sub_questions=[],
        research_plan="",
        findings=[],
        contradictions=[],
        credibility_scores=[],
        synthesis="",
        confidence=0.0,
        sources=[],
        thinking_log=[]
    )
    return graph.invoke(initial_state)

if __name__ == "__main__":
    print("Script started...")
    result = run("Is AI replacing jobs or creating new ones?")
    print("Raw result keys:", result.keys())
    print("Thinking log:", result.get("thinking_log"))
    print("Synthesis:", result.get("synthesis"))