from enum import Enum, auto


class MessageType(Enum):
    SMS = auto()
    EMAIL = auto()
    WHATSAPP = auto()
    TELEGRAM = auto()
