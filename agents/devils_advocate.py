import os
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
from core.chroma_store import store
from utils.logger import log

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def devils_advocate_node(state):
    contradictions = []
    for i, q in enumerate(state.sub_questions[:2]):
        counter_query = f"criticism against or counterargument to: {q}"
        results = tavily.search(query=counter_query, max_results=2)
        if not results.get("results"):
            continue
        for j, r in enumerate(results["results"]):
            doc_id = f"counter_{i}_{j}"
            store(doc_id, r["content"], {"url": r["url"], "type": "contradiction"})
            contradictions.append({"question": q, "url": r["url"], "content": r["content"][:500]})
    state.contradictions = contradictions
    state = log(state, "Devil's Advocate", f"Found {len(contradictions)} contradictions")
    return state
