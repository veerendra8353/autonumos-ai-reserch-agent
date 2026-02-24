import json
import re
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from core.chroma_store import retrieve
from utils.logger import log

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

# RESEARCHER PROMPT TEMPLATE - Forces deep research behavior
RESEARCHER_TEMPLATE = '''Act as a specialist researcher, not a chatbot.

Conduct a comprehensive and structured research study on the topic: "{TOPIC}"

Follow these rules strictly:
- Do NOT give short or direct answers.
- Avoid bullet-only or superficial explanations.
- Do NOT assume the reader already understands the topic.

Your response MUST follow this structure:

1. Research Framing
Explain what the topic is, why it matters, and what problem or domain it belongs to.

2. Core Mechanism / Foundations
Explain how it works in detail.
Break down the underlying concepts, processes, or systems step by step.

3. Current Developments, Debates, or Trends
Analyze recent advancements, open challenges, controversies, or competing viewpoints in this field.

4. Multi-Layered Impact Analysis
Discuss the topic's:
- Technical implications
- Social or ethical implications
- Economic or industry impact

5. Evidence & Source Guidance
List at least three high-authority sources or institutions (e.g., research labs, universities, standards bodies, government agencies, major companies) that are relevant for further study.
Explain why each source is credible.

6. Synthesis & Confidence
Summarize the findings into a coherent conclusion.
State a confidence level (High / Medium / Low) and explain any uncertainty or gaps.

Important constraints:
- Minimum depth is required; shallow responses are unacceptable.
- If information is limited, explain what is missing instead of guessing.
- Prefer clarity and completeness over speed.

Use this evidence from web search:
{EVIDENCE}

Return your response as JSON with this structure:
{{
  "research_framing": "...",
  "core_mechanism": "...",
  "developments": "...",
  "impact_analysis": "...",
  "sources": [
    {{"name": "...", "credibility": "..."}},
    {{"name": "...", "credibility": "..."}},
    {{"name": "...", "credibility": "..."}}
  ],
  "synthesis": "...",
  "confidence_level": "High|Medium|Low",
  "confidence_reason": "..."
}}'''

def safe_parse(text):
    """Extract and parse JSON from LLM response"""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except json.JSONDecodeError:
        pass
    return {}

def synthesizer_node(state):
    """Synthesizer uses Researcher Prompt Template for deep, structured analysis."""
    context = retrieve(state.query, n=8)
    context_text = "\n".join(context) if context else "No additional evidence retrieved."
    
    # Inject topic into Researcher Template
    prompt = RESEARCHER_TEMPLATE.format(TOPIC=state.query, EVIDENCE=context_text)
    
    state = log(state, "Synthesizer", "Executing deep research synthesis...")
    response = llm.invoke(prompt)
    data = safe_parse(response.content)
    
    # Build comprehensive synthesis from all 6 sections
    synthesis_parts = []
    if data.get("research_framing"):
        synthesis_parts.append(f"## 1. Research Framing\n{data['research_framing']}")
    if data.get("core_mechanism"):
        synthesis_parts.append(f"\n## 2. Core Mechanism\n{data['core_mechanism']}")
    if data.get("developments"):
        synthesis_parts.append(f"\n## 3. Developments & Debates\n{data['developments']}")
    if data.get("impact_analysis"):
        synthesis_parts.append(f"\n## 4. Impact Analysis\n{data['impact_analysis']}")
    if data.get("sources"):
        sources_text = "\n".join([f"- **{s.get('name', 'Unknown')}**: {s.get('credibility', '')}" for s in data["sources"]])
        synthesis_parts.append(f"\n## 5. Sources\n{sources_text}")
    if data.get("synthesis"):
        synthesis_parts.append(f"\n## 6. Synthesis\n{data['synthesis']}")
    
    full_synthesis = "\n\n".join(synthesis_parts)
    
    # Map confidence level to numeric score
    confidence_map = {"High": 0.9, "Medium": 0.6, "Low": 0.3}
    confidence_level = data.get("confidence_level", "Medium")
    confidence_score = confidence_map.get(confidence_level, 0.6)
    
    state.synthesis = full_synthesis if full_synthesis else data.get("synthesis", "No synthesis generated")
    state.confidence = confidence_score
    state._synthesis_data = data
    
    state = log(state, "Synthesizer", f"Research complete. Confidence: {confidence_level} ({int(confidence_score * 100)}%)")
    return state
