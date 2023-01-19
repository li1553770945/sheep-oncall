import json
from enum import Enum


class EventType(Enum):
    USER_REGISTER = 0
    PRIVATE_MESSAGE = 1
    GROUP_MESSAGE = 2


class Event:
    def __init__(self, event_type, from_user_id, to_user_id, content):
        self.type = event_type
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content
        self.topic = ""

    def __str__(self):
        return json.dumps(self)
