from enum import Enum


class MessageType(Enum):
    HUMAN = "human"
    TOOL = "tool"
    SYSTEM = "system"
    AI = "ai"
