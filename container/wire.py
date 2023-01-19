from infra.config.config_loader import config_provider
from infra.database.mysql import database_provider
from internal.service.event_dispatch.message_dispatch import event_dispatch_provider
from internal.client.zulip_client import zulip_client_provider
from infra.logger.logger import logger

class Container:
    def __init__(self, config_file="config.ini"):
        logger.info("initialing config")
        config = config_provider(config_file)
        logger.info("initialing database")
        database = database_provider(config)
        logger.info("initialing event dispatch")
        event_dispatcher = event_dispatch_provider(config)
        logger.info("program running")
        self.zulip_client = zulip_client_provider(config_file, event_dispatcher)


def InitContainer():
    return Container()