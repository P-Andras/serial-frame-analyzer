from enum import Enum

class MsgClass(Enum):
    SYSTEM = 0x01
    DFU = 0x02
    ENDPOINT = 0x03
    HARDWARE = 0x04

class SystemID(Enum):
    HELLO = 0x01
    RESET = 0x02
    GET_COUNTERS = 0x03
    