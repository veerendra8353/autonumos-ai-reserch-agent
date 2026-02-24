import streamlit as st
import time
from datetime import datetime

# -------------------------------
# CSS (GLASS + COLORS)
# -------------------------------
def inject_thinking_log_css():
    st.markdown("""
    <style>
    .thinking-panel {
      position: sticky;
      top: 10px;
    }

    .thinking-card {
      background: rgba(20, 10, 40, 0.75);
      backdrop-filter: blur(14px);
      border-radius: 14px;
      padding: 0.9rem;
      margin-bottom: 0.6rem;
      border-left: 4px solid #64748b;
      animation: fadeIn 0.4s ease-in;
    }

    .step-plan { border-left-color: #38bdf8; }
    .step-search { border-left-color: #a78bfa; }
    .step-analyze { border-left-color: #facc15; }
    .step-validate { border-left-color: #22c55e; }
    .step-revise { border-left-color: #ef4444; }
    .step-synthesize { border-left-color: #22c55e; }

    .step-active {
      box-shadow: 0 0 20px rgba(167,139,250,0.35);
    }

    .step-meta {
      font-family: monospace;
      font-size: 0.75rem;
      opacity: 0.7;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


# -------------------------------
# THINKING LOG UI RENDER
# -------------------------------
def render_thinking_log(thinking_steps):
    """
    Renders the Thinking Log UI component based on a list of steps.
    """
    if not thinking_steps:
        st.markdown(
            "<div style='color: #71717a; font-size: 0.9rem; font-style: italic; text-align: center; margin-top: 2rem;'>Agent is idle...</div>", 
            unsafe_allow_html=True
        )
        return

    # Determine the "active" step: usually the last step in the list if its status is running/not complete
    current_step_id = None
    if thinking_steps and thinking_steps[-1].get("status") != "complete" and thinking_steps[-1].get("status") != "completed":
        current_step_id = thinking_steps[-1].get("step_number")

    for step in thinking_steps:
        step_id = step.get("step_number")
        is_active = "step-active" if step_id == current_step_id else ""
        step_type = step.get("type", "Plan")
        step_class = f"thinking-card step-{step_type.lower()} {is_active}"

        st.markdown(f"""
        <div class="{step_class}">
          <b>Step {step_id} — {step_type}</b><br/>
          {step.get('description', '')}<br/>
          <div class="step-meta">
            Tool: {step.get('tool') or "—"} |
            Status: {step.get('status', 'running')} |
            {step.get('timestamp', '')}
          </div>
        </div>
        """, unsafe_allow_html=True)
