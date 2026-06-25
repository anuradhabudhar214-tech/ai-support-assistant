import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

cases = [
    ("Where is my order ORD-58213?", "default1"),
    ("I want a refund for my last purchase", "default2"),
    ("I have a complaint about your service", "default3"),
    ("I want to speak to a manager", "default4"),
    ("Show hotels in Dubai", "memcheck"),
    ("Show cheaper ones", "memcheck"),  # follow-up, should reuse hotel_search intent
    ("Find me flights to Dubai", "default6"),
    ("asdkjf random gibberish", "default7"),
]

all_ok = True
for message, session_id in cases:
    resp = client.post("/chat", json={"message": message, "session_id": session_id})
    print(f"--- {session_id} | {message!r} -> status {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        all_ok = False
        continue
    body = resp.json()
    print(json.dumps(body, indent=2))
    # basic schema checks
    for key in ["intent", "tool_called", "ui_type", "message", "data", "session_id", "turn"]:
        assert key in body, f"missing key {key}"

print("\nALL CHECKS PASSED" if all_ok else "\nSOME CHECKS FAILED")
