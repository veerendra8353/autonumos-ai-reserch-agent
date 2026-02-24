import json
import re
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from utils.logger import log

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def safe_parse(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return json.loads(match.group()) if match else {}

def validator_node(state):
    scores = []
    for source in state.sources[:5]:
        template = '''Rate the credibility of this source URL from 1-10.
Source: {source}
Return JSON only: {{ "url": "{source}", "score": 7, "reason": "..." }}'''
        prompt = template.format(source=source)
        response = llm.invoke(prompt)
        data = safe_parse(response.content)
        if data:
            scores.append(data)
        else:
            scores.append({"url": source, "score": 5, "reason": "Could not assess"})
    state.credibility_scores = scores
    avg = sum(s["score"] for s in scores) / len(scores) if scores else 5
    state = log(state, "Fact Validator", f"Scored {len(scores)} sources. Avg credibility: {avg:.1f}/10")
    return state
