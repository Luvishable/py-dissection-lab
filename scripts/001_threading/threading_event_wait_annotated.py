"""
Goal:
----
Demonstrate a clean coordination pattern between threads using threading.Event()

Key Idea
--------
- A threading.Event is a thread-safe synchronization mechanism
- One thread can signal the event via set()
- Other threads can be blocked until that signal arrives via wait()

In this script:
- The worker thread sleeps for 3 seconds, then signals the event.
- The main thread blocks on event.wait() until the worker sends the signal
- Finally, the main thread execute join()'s the worker to ensure a graceful shutdown
"""


import threading
import time

# `Event` is a synchronization object shared between threads.
# Think of it as a boolean flag managed in a thread-safe way:
# Initially: "not set" (False)
# After calling set(), it becomes True and all waiters are released.
stop_event = threading.Event()

def worker():
    """
    Important:
    - `stop_event.set()` does not kill/stop threads by itself.
       It only changes the Event's state to "set" and wakes threads waiting on it.
    - We still decide what to do after the signal (e.g., exit a loop, cleanup, etc.).
    """
    print("Worker started, will be stopped 3 secs later...")
    time.sleep(3)   # Simulation of a work. Releases the GIL during the sleep
    stop_event.set()    # Signal: event state becomes "set" and waiting threads are released
    print("Worker executed stop_event.set()")

# target=worker means that run the worker function in a new OS-level thread managed by Python
t = threading.Thread(target=worker)
t.start()

print("Main: I am waiting for stop_event)")
# Block the main thread until the event is set.
# - If the event is already set, wait() returns immediately
# - Otherwise, it blocks until some thread calls stop_event.set()
stop_event.wait()
print("Main: stop_event got set so I am carrying on")

# Ensure the worker thread has finished before exiting the program.
# Even though the event has been set, joining is a good practice to:
# - avoid leaving background work incomplete
# - ensure a clean, deterministic shutdown
t.join()

