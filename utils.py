import json

def tracks_to_json(tracks):
    return json.dumps(tracks, ensure_ascii=False)

def tracks_from_json(s):
    try:
        return json.loads(s)
    except:
        return []
