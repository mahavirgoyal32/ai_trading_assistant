import json

def safe_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return {}
