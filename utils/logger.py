from datetime import datetime

def log(state, agent_name, message, step_type="Plan"):
    """
    Logs a structured thinking step. 
    step_type should be one of: Plan, Search, Analyze, Validate, Revise, Synthesize
    """
    if not hasattr(state, "thinking_log") or state.thinking_log is None:
        state.thinking_log = []
        
    step_num = len(state.thinking_log) + 1
    
    # Map agent to type heuristically if not explicitly provided
    if step_type == "Plan":
        if agent_name == "Director": step_type = "Plan"
        elif agent_name == "Researcher": step_type = "Search"
        elif "Advocate" in agent_name: step_type = "Analyze"
        elif agent_name == "Fact Validator": step_type = "Validate"
        elif agent_name == "Synthesizer": step_type = "Synthesize"
    
    step = {
        "step_number": step_num,
        "type": step_type,
        "description": message,
        "tool": agent_name,
        "status": "completed",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    state.thinking_log.append(step)
    return state
