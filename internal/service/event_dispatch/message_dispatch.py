import queue
from concurrent.futures import ThreadPoolExecutor
from infra.config.config_loader import Config
from threading import BoundedSemaphore


class EventDispatch:
    def __init__(self, config: Config):
        self.q = queue.Queue()
        self.s = BoundedSemaphore(0)
        with ThreadPoolExecutor(max_workers=int(config.get("thread", "num_works"))) as t:
            for i in range(0, int(config.get("thread", "num_works"))):
                t.submit(self.dispatch_event)

    def add_event(self, event):
        self.q.put(event)
        self.s.release()
        pass

    def dispatch_event(self):
        while True:
            self.s.acquire()
            message = self.q.get()


def event_dispatch_provider(config: Config):
    return EventDispatch(config)
