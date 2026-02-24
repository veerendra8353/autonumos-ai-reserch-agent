from langgraph.graph import StateGraph, END, START
from core.state import ResearchState
from agents.director import director_node
from agents.researcher import researcher_node
from agents.devils_advocate import devils_advocate_node
from agents.validator import validator_node
from agents.synthesizer import synthesizer_node

def build_graph():
    graph = StateGraph(ResearchState)
    
    # Add all agent nodes
    graph.add_node("director", director_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("devils_advocate", devils_advocate_node)
    graph.add_node("validator", validator_node)
    graph.add_node("synthesizer", synthesizer_node)
    
    # Define the research workflow
    graph.add_edge(START, "director")
    graph.add_edge("director", "researcher")
    graph.add_edge("researcher", "devils_advocate")
    graph.add_edge("devils_advocate", "validator")
    graph.add_edge("validator", "synthesizer")
    graph.add_edge("synthesizer", END)
    
    return graph.compile()
