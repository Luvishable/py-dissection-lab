import threading
import time

stop_event = threading.Event()

def worker():
    print("Worker başladı, 3 saniye sonra durduracağım.")
    time.sleep(3)
    stop_event.set()
    print("Worker stop_event.set() yaptı.")

t = threading.Thread(target=worker)
t.start()

print("Main: stop_event bekliyor...")
stop_event.wait()
print("Main: stop_event geldi, devam ediyorum.")

t.join()
