# Simple in-memory storage for chroma documents
_storage = {}
_metadata = {}

def store(doc_id, content, meta):
    _storage[doc_id] = content
    _metadata[doc_id] = meta
    return doc_id

def retrieve(query, n=5):
    # Simple retrieval - return all stored content
    results = []
    for doc_id, content in _storage.items():
        results.append(content)
    return results[:n]

def get_metadata(doc_id):
    return _metadata.get(doc_id, {})
