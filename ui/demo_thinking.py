import streamlit as st
import time
from thinking_log import (
    render_thinking_log, 
    add_step, 
    update_step_status, 
    clear_thinking_log,
    inject_thinking_log_css
)

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Autonomous Agent Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "demo_running" not in st.session_state:
    st.session_state.demo_running = False

def run_mock_agent():
    """Simulates an autonomous AI agent thinking process emitting events."""
    st.session_state.demo_running = True
    clear_thinking_log()
    
    # We use a placeholder in the sidebar to re-render the log without full script reruns
    log_placeholder = st.sidebar.empty()
    
    def render():
        with log_placeholder.container():
            st.markdown("<div class='thinking-log-title'>🧠 Agent Thinking Log</div>", unsafe_allow_html=True)
            render_thinking_log(st.session_state.thinking_steps)

    # Step 1: Plan
    idx = add_step(
        "Plan", 
        "Formulating a multi-step research plan based on the user's query about 'Quantum Computing breakthroughs 2024'.",
        tool="PlannerAgent"
    )
    render()
    time.sleep(2.0)
    update_step_status(idx, "completed")
    
    # Step 2: Search
    idx = add_step(
        "Search", 
        "Executing parallel queries across ArXiv and general web indices for recent papers.",
        tool="TavilySearch"
    )
    render()
    time.sleep(3.0)
    update_step_status(idx, "completed", "Found 14 relevant sources from ArXiv and tech journals.")
    
    # Step 3: Analyze
    idx = add_step(
        "Analyze", 
        "Extracting key claims from sources. Identifying contradictions between Microsoft and IBM roadmaps.",
        tool="DataExtractor"
    )
    render()
    time.sleep(4.0)
    update_step_status(idx, "completed")
    
    # Step 4: Validate
    idx = add_step(
        "Validate", 
        "Cross-referencing claims about 1000+ qubit coherence times. Checking credibility of preprint sources.",
        tool="FactChecker"
    )
    render()
    time.sleep(2.5)
    update_step_status(idx, "completed", "1 claim rejected due to low credibility source. 13 verified.")
    
    # Step 5: Revise
    idx = add_step(
        "Revise", 
        "Missing context on topological qubits. Spawning sub-agent to retrieve specific papers from early 2024.",
        tool="SubQueryGenerator"
    )
    render()
    time.sleep(2.5)
    update_step_status(idx, "completed")
    
    # Step 6: Search (Sub-query)
    idx = add_step(
        "Search", 
        "Querying 'topological qubits Microsoft ANY 2024'...",
        tool="TavilySearch"
    )
    render()
    time.sleep(2.0)
    update_step_status(idx, "completed")
    
    # Step 7: Synthesize
    idx = add_step(
        "Synthesize", 
        "Drafting final report: Combining verified claims, organizing by timeline, and resolving contradictions.",
        tool="ReportWriter"
    )
    render()
    time.sleep(3.5)
    update_step_status(idx, "completed", "Final integration complete. Confidence score: 92%.")
    render()
    
    st.session_state.demo_running = False

# ---------------- MAIN UI ----------------

# Inject CSS globally so sidebar inherits it
inject_thinking_log_css()

# Sidebar: Thinking Log
with st.sidebar:
    # If not running, just show what's there
    if not st.session_state.demo_running:
        st.markdown("<div class='thinking-log-title'>🧠 Agent Thinking Log</div>", unsafe_allow_html=True)
        if "thinking_steps" in st.session_state:
            render_thinking_log(st.session_state.thinking_steps)
        else:
            render_thinking_log([])

# Main Content Area
st.title("Search & Synthesis Agent")
st.markdown("This demo shows how to use Streamlit placeholders to display a real-time, side-by-side thinking log without blocking or needing React/WebSockets.", unsafe_allow_html=True)

query = st.text_input("Enter research topic", "Recent advancements in Quantum Computing 2024")

if st.button("🚀 Start Autonomous Research", type="primary", disabled=st.session_state.demo_running):
    run_mock_agent()
    st.rerun()

# Show mock result if completed
if "thinking_steps" in st.session_state and len(st.session_state.thinking_steps) == 7 and not st.session_state.demo_running:
    st.success("✅ Research Complete!")
    st.markdown("### Findings")
    st.write("1. **IBM Condor**: ...")
    st.write("2. **Microsoft Topological Focus**: ...")
    st.balloons()
