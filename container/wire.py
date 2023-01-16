from infra.config.config_loader import config_provider
from infra.database.mysql import database_provider
from internal.service.event_dispatch.message_dispatch import event_dispatch_provider
from internal.client.zulip_client import zulip_client_provider


class Container:
    def __init__(self, config_file="config.ini"):
        self.config = config_provider(config_file)
        self.database = database_provider(self.config)
        self.event_dispatch = event_dispatch_provider(self.config)
        self.zulip_client = zulip_client_provider(config_file, self.event_dispatch.dispatch_event)
