from classes.conversation_participant import ConversationParticipant
from constants.default import USER_RESERVED_NAME
from models.conversation_message import ConversationMessage


class Conversation:
    def __init__(self, participants: list[ConversationParticipant], messages: list[ConversationMessage] = None, current_turn: int = 0, max_rounds: int = 5, current_round: int = 0):
        self.participants = participants
        self.messages: list[ConversationMessage] = messages if messages is not None else []
        self.current_turn = current_turn
        self.current_round = current_round
        self.max_rounds = max_rounds

    def process_conversation_round(self):
        for i in range(len(self.participants)):
            self.current_turn += 1
            participant = self.participants[i]
            message_content = participant.conversation(self.messages).run().get_result()
            self.add_message(ConversationMessage(author=participant.name, content=message_content))

        self.current_round += 1
        return self
    
    def get_last_round_messages(self) -> list[ConversationMessage]:
        if self.current_round == 0:
            return []
        
        messages_per_round = len(self.participants)

        return self.messages[-messages_per_round:]

    def add_user_message(self, content: str):
        self.add_message(ConversationMessage(author=USER_RESERVED_NAME, content=content))
        return self

    def set_max_rounds(self, max_rounds: int):
        self.max_rounds = max_rounds

    def set_current_round(self, current_round: int):
        self.current_round = current_round
        return self
    
    def get_current_round(self) -> int:
        return self.current_round

    def get_max_rounds(self) -> int:
        return self.max_rounds

    def set_current_turn(self, current_turn: int):
        self.current_turn = current_turn

    def get_current_turn(self) -> int:
        return self.current_turn

    def get_participants(self) -> list[ConversationParticipant]:
        return self.participants

    def get_participant_by_name(self, name: str) -> ConversationParticipant | None:
        for participant in self.participants:
            if participant.name == name:
                return participant
        return None

    def add_participant(self, participant: ConversationParticipant):
        self.participants.append(participant)

    def remove_participant(self, name: str) -> bool:
        for i, participant in enumerate(self.participants):
            if participant.name == name:
                del self.participants[i]
                return True
        return False
    
    def insert_participant(self, index: int, participant: ConversationParticipant):
        self.participants.insert(index, participant)
        return self
    
    def add_message(self, message: ConversationMessage):
        self.messages.append(message)

    def get_messages(self) -> list[ConversationMessage]:
        return self.messages

    def set_messages(self, messages: list[ConversationMessage]):
        self.messages = messages
        return self

    def insert_message(self, index: int, message: ConversationMessage):
        self.messages.insert(index, message)
        return self

    def remove_message(self, message: ConversationMessage) -> bool:
        if message in self.messages:
            self.messages.remove(message)
            return True
        return False

    def reset(self):
        self.participants.clear()
        self.messages.clear()
        return self
    
    