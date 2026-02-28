import hashlib

def make_cache_key(query: str) -> str:
    hashed = hashlib.sha256(query.strip().encode("utf-8")).hexdigest()
    return f"analysis:{hashed}"