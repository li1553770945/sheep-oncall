from internal.client.client_base import Client
from internal.domain.event import Event
import zulip


class Zulip(Client):
    def __init__(self, config_file, event_callback):
        super().__init__()
        self.client = zulip.Client(config_file=config_file)
        self.client.call_on_each_event(self.callback)
        self.event_callback = event_callback

    def callback(self, e):
        event = Event("", "", "", "")
        self.event_callback(event)

    def login(self):
        pass


def zulip_client_provider(config_file, callback_func):
    return Zulip(config_file, callback_func)
