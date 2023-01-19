from internal.client.client_base import Client
from internal.domain.event import Event, EventType
import zulip
from infra.logger.logger import logger


class Zulip(Client):
    def __init__(self, config_file, event_dispatcher):
        super().__init__()
        self.client = zulip.Client(config_file=config_file)
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.send_private_message = self.send_private_message
        self.event_dispatcher.send_group_message = self.send_group_message
        self.bot_id = self.client.get_profile()['user_id']

        self.client.call_on_each_event(self.callback)

    def callback(self, e):
        print(e)
        event = Event("", "", "", "")
        if e["type"] == "realm_user" and e['op'] == "add":
            event.type = EventType.USER_REGISTER.value
            event.from_user_id = e['person']['user_id']
        elif e['type'] == "message" and e['message']['type'] == "private" and e['message']['sender_id'] != self.bot_id:
            event.type = EventType.PRIVATE_MESSAGE.value
            event.from_user_id = e['message']['sender_id']
            event.content = e['message']['content']
        elif e['type'] == "message" and e['message']['type'] == "stream" and e['message']['sender_id'] != self.bot_id:
            event.type = EventType.GROUP_MESSAGE.value
            event.from_user_id = e['message']['sender_id']
            event.content = e['message']['content']
            event.to_user_id = e['message']['stream_id']
            event.topic = e['message']['subject']
        else:
            return
        self.event_dispatcher.add_event(event)

    def login(self):
        pass

    def send_private_message(self, to_user_id, content):
        request = {
            "type": "private",
            "to": [to_user_id],
            "content": content,
        }
        result = self.client.send_message(request)
        if result['result'] != "success":
            logger.error("send private message error:" + str(result))

    def send_group_message(self, to_group_id, content, topic):
        request = {
            "type": "stream",
            "to": [to_group_id],
            "content": content,
            "topic": topic
        }
        result = self.client.send_message(request)
        if result['result'] != "success":
            logger.error("send group message error:" + str(result))


def zulip_client_provider(config_file, event_dispatcher):
    return Zulip(config_file, event_dispatcher)
