import time, httpx

url = "http://localhost:8000/api/courses/popular"

for _ in range(600):
    try:
        r = httpx.get(url)
        if r.status_code == 200:
            print("✅ Backend is UP")
            break
    except Exception:
        print("⏳ Waiting...")
    time.sleep(1)
else:
    raise RuntimeError("❌ Backend didn't respond")
