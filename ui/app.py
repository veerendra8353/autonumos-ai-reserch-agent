"""
AutoResearch Agent - CUSTOM FONT EDITION
Hero + Sticky Title with HelloChristmas font
"""

import streamlit as st
from dotenv import load_dotenv
import sys
import os
import time

# Add parent directory to path so absolute imports like `ui.thinking_log` work
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ui.thinking_log import render_thinking_log, inject_thinking_log_css

# Load environment variables
load_dotenv()

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Autonomous AI Research Agent",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD CSS ----------------
css_path = os.path.join(os.path.dirname(__file__), "styles", "app.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "research_result" not in st.session_state:
    st.session_state.research_result = None
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# Inject CSS globally so sidebar inherits it
inject_thinking_log_css()

# Sidebar: Thinking Log
with st.sidebar:
    st.markdown("<div class='thinking-log-title'>🧠 Agent Thinking Log</div>", unsafe_allow_html=True)
    log_placeholder = st.empty()
    
    # render current log if it exists and app not running
    if not st.session_state.is_running and st.session_state.research_result:
        result_dict = st.session_state.research_result if isinstance(st.session_state.research_result, dict) else st.session_state.research_result.__dict__
        with log_placeholder.container():
            render_thinking_log(result_dict.get('thinking_log', []))
    elif not st.session_state.is_running:
        with log_placeholder.container():
            render_thinking_log([])

# ---------------- HERO (NORMAL VIEW) ----------------
st.markdown("""
<div class="hero-card">
  <div class="hero-title">
    Autonomous <span class="hero-gradient">AI Research</span> Agent
  </div>
  <div class="hero-sub">
    🔮 Watches itself think, plan, search, validate, and synthesize
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SEARCH INPUT ----------------
query = st.text_input(" ", placeholder="🔍 Enter any topic to research...")


# Alternative: Use Streamlit button for functionality
if st.button("🚀 Start Deep Research", use_container_width=True, type="primary"):
    if query:
        st.session_state.is_running = True
        
        # Add parent directory to path
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from core.build_graph import build_graph
        from core.state import ResearchState
        
        # Build graph
        with st.spinner("🔮 Initializing AI agents..."):
            graph = build_graph()
        st.toast("✅ Multi-agent system ready", icon="🤖")
        
        # Execute research
        with st.spinner("🧠 Processing research..."):
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
            
            # Use stream for real-time updates
            result = None
            for step_state in graph.stream(initial_state):
                state_val = list(step_state.values())[0] if isinstance(step_state, dict) else step_state
                thinking_log = state_val.get('thinking_log', []) if isinstance(state_val, dict) else getattr(state_val, 'thinking_log', [])
                
                # Update UI
                with log_placeholder.container():
                    render_thinking_log(thinking_log)
                result = state_val
                
            # If for some reason stream didn't run, fallback
            if not result:
                result = graph.invoke(initial_state)
                thinking_log = result.get('thinking_log', []) if isinstance(result, dict) else getattr(result, 'thinking_log', [])
                with log_placeholder.container():
                    render_thinking_log(thinking_log)
        
        st.session_state.research_result = result
        st.session_state.is_running = False
        st.balloons()
        st.success("✅ Research Complete!")

# ---------------- DISPLAY RESULTS ----------------
if st.session_state.research_result:
    result = st.session_state.research_result
    
    # Convert dataclass to dict
    result_dict = result if isinstance(result, dict) else {
        'query': result.query,
        'sub_questions': result.sub_questions,
        'research_plan': result.research_plan,
        'findings': result.findings,
        'contradictions': result.contradictions,
        'credibility_scores': result.credibility_scores,
        'synthesis': result.synthesis,
        'confidence': result.confidence,
        'sources': result.sources,
        'thinking_log': result.thinking_log
    }
    
    # ---------------- STICKY TITLE (SCROLL MODE) ----------------
    st.markdown("""
    <div class="sticky-research-title">
      AUTONOMOUS AI RESEARCH BOT
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------- RESEARCH SYNTHESIS ----------------
    st.markdown(f"""
    <div class="research-synthesis">
      <h3 style="margin-top: 0; color: #22c55e; font-size: 1.2rem;">✨ FINAL SYNTHESIS</h3>
      {result_dict['synthesis'] or 'No synthesis generated'}
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------- METRICS ----------------
    metric_cols = st.columns(4)
    
    metrics = [
        (f"{int(result_dict['confidence'] * 100)}%", "Confidence"),
        (str(len(result_dict.get('sub_questions', []))), "Sub-Questions"),
        (str(len(result_dict.get('sources', []))), "Sources"),
        (str(len(result_dict.get('contradictions', []))), "Contradictions")
    ]
    
    for col, (value, label) in zip(metric_cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value">{value}</div>
              <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ---------------- DUMMY CONTENT FOR SCROLL (for testing sticky) ----------------
    for i in range(8):
        st.markdown(f"""
        <div class="content-card">
          <h3>Research Section {i+1}</h3>
          <p>
            This section simulates long research output so you can
            see the sticky title lock into the top-left corner while scrolling.
            The custom HelloChristmas font should be visible in the sticky title above.
          </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------- SOURCES ----------------
    if result_dict.get('sources'):
        with st.expander("🔗 All Sources Referenced"):
            for src in result_dict['sources']:
                st.markdown(f'<div style="color: #a78bfa; font-size: 0.9rem; padding: 0.25rem 0;">• {src}</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.5; font-size: 0.85rem;">
    <p style="color: #a1a1aa;">Built with 🔮 LangGraph • 🧠 Groq • 🔍 Tavily • 💜 Streamlit</p>
</div>
""", unsafe_allow_html=True)
