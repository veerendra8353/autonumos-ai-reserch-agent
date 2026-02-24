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

def director_node(state):
    template = '''You are a research director. Break this query into exactly 4 sub-questions for deep research.
Query: {query}
Return JSON only: {{"research_plan": "...", "sub_questions": ["...", "...", "...", "..."]}}'''
    prompt = template.format(query=state.query)
    response = llm.invoke(prompt)
    data = safe_parse(response.content)
    state.research_plan = data.get("research_plan", "")
    state.sub_questions = data.get("sub_questions", [])
    state = log(state, "Director", f"Created {len(state.sub_questions)} sub-questions")
    return state
