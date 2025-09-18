
from classes.base_llm_connector import BaseLLMConnector
from constants.default import USER_RESERVED_NAME

from models.conversation_message import ConversationMessage

class ConversationParticipant:
    def __init__(self, participant_id: str, name: str, llm_instance: BaseLLMConnector):
        self.participant_id = participant_id
        self.name = name
        if not llm_instance or not isinstance(llm_instance, BaseLLMConnector):
            raise ValueError("llm_instance required and must be an instance of BaseLLMConnector")

        self._llm_instance = llm_instance

    def _format_message(self, message: ConversationMessage):
        if (message.author == USER_RESERVED_NAME):
            return {"role": "user", "content": message.content}
        if (message.author == self.name):
            return {"role": "assistant", "content": message.content}
        return {"role": "user", "content": f"[{message.author}]: {message.content}"}
    
    def _get_formatted_messages(self, messages: list[ConversationMessage]):
        return [self._format_message(msg) for msg in messages]

    def conversation(self, messages: list[ConversationMessage]):
        formatted_messages = self._get_formatted_messages(messages)        
        return self._llm_instance.conversation(formatted_messages)
    
    def __getattr__(self, name):
        return getattr(self._llm_instance, name)