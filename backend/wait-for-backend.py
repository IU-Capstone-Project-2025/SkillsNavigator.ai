import time
import os

TARGET = "Successful course download to Qdrant"
LOG_PATH = "/app/log.log"
TIMEOUT = 600  # 10 минут


print("👀 Waiting for backend log:", TARGET)

with open("/app/log.log", "w") as f:
    f.write("")

start_time = time.time()

while True:
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            lines = f.read()
            if TARGET in lines:
                print("✅ Log phrase found!")
                break

    if time.time() - start_time > TIMEOUT:
        print("❌ Timeout: log line not found.")
        exit(1)

    print("⏳ Still waiting for log...")
    time.sleep(10)
