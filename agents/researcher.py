import os
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
from core.chroma_store import store
from utils.logger import log

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def researcher_node(state):
    findings = []
    for i, q in enumerate(state.sub_questions):
        results = tavily.search(query=q, max_results=3)
        if not results.get("results"):
            continue
        for j, r in enumerate(results["results"]):
            doc_id = f"finding_{i}_{j}"
            store(doc_id, r["content"], {"url": r["url"], "question": q})
            findings.append({"question": q, "url": r["url"], "content": r["content"][:500]})
    state.findings = findings
    state.sources = list(set(f["url"] for f in findings))
    state = log(state, "Researcher", f"Found {len(findings)} results across {len(state.sub_questions)} questions")
    return state
