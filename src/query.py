import requests
import time

def get_fact():
    b = time.time()
    resp = requests.get("https://catfact.ninja/fact")
    resp.raise_for_status()
    resp_json = resp.json()
    query_time = time.time() - b
    return {
        "query_time": query_time,
        "length": resp_json["length"],
        "fact": resp_json["fact"],
        "status": 200,
        "dot_end": resp_json["fact"][-1] == ".",
    }

print(get_fact())