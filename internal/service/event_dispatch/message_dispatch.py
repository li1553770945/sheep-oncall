import queue
from concurrent.futures import ThreadPoolExecutor
from infra.config.config_loader import Config
from threading import Semaphore
from infra.logger.logger import logger
from internal.domain.event import EventType


class EventDispatch:

    def __init__(self, config: Config):
        self.q = queue.Queue()
        self.s = Semaphore(0)
        thread_pool = ThreadPoolExecutor(max_workers=int(config.get("thread", "num_works")))
        for i in range(0, int(config.get("thread", "num_works"))):
            thread_pool.submit(self.dispatch_event)
        self.send_private_message = self.default_send_private_func
        self.send_group_message = self.default_send_group_func

    def add_event(self, event):
        self.q.put(event)
        self.s.release()
        pass

    def dispatch_event(self):
        logger.info("dispatch thread start")
        while True:
            self.s.acquire()
            event = self.q.get()

            if event.type == EventType.USER_REGISTER.value:
                self.send_private_message(event.from_user_id, "welcome!")
            elif event.type == EventType.PRIVATE_MESSAGE.value:
                self.send_private_message(event.from_user_id, "reply:" + event.content)
                pass
            elif event.type == EventType.GROUP_MESSAGE.value:
                self.send_group_message(event.to_user_id, "reply:" + event.content,event.topic)
                pass
            else:
                logger.warn("unknown event type:" + str(event.type))

    def default_send_private_func(self, user_id, content):
        raise TypeError("you have not set the function \"send_private_message\"")

    def default_send_group_func(self, user_id, content,topic):
        raise TypeError("you have not set the function \"send_group_message\"")


def event_dispatch_provider(config: Config):
    return EventDispatch(config)
