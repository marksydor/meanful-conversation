from dataclasses import dataclass

@dataclass
class ConversationMessage:
    author: str
    content: str
