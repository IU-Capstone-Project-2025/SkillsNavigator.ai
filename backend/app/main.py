import threading

if __name__ == '__main__':
    print("Hello from backend!", flush=True)
    stop_event = threading.Event()
    stop_event.wait()
