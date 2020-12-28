from collections import namedtuple
from enum import Enum


class Keys(Enum):
    "Enumeration of all the badge's keys."

    BTN_UP = 0
    BTN_RIGHT = 1
    BTN_DOWN = 2
    BTN_LEFT = 3
    BTN_A = 4
    BTN_B = 5
    BTN_SELECT = 6
    BTN_START = 7


"An event is the tuple of a key bound with an action."
Event = namedtuple("Event", ["key", "is_push"])


def unpack_event(data):
    "Create an event from bytes."
    cmd = int(data[0])
    return Event(key=Keys(cmd & 0x0F), is_push=bool(cmd >> 4))
