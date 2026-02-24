import os
from dotenv import load_dotenv
load_dotenv()

from core.build_graph import build_graph
from core.state import ResearchState

def test_stream():
    graph = build_graph()
    initial_state = ResearchState(
        query="What is the speed of light?",
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
    
    print("Testing stream...")
    count = 0
    for chunk in graph.stream(initial_state):
        print(f"Chunk {count}: {type(chunk)}")
        if isinstance(chunk, dict):
            node_name = list(chunk.keys())[0]
            node_state = chunk[node_name]
            print(f"  Node: {node_name}")
            print(f"  State type: {type(node_state)}")
            if isinstance(node_state, dict):
                tl = node_state.get('thinking_log')
            else:
                tl = getattr(node_state, 'thinking_log', None)
            print(f"  Thinking Log size: {len(tl) if tl else 0}")
        count += 1

if __name__ == "__main__":
    test_stream()
