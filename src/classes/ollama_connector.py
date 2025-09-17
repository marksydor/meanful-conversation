import ollama

from classes.base_llm_connector import BaseLLMConnector
from constants.default import ASISTANT_SYSTEM_PROMPT, MODEL_LLAMA

class OllamaConnector(BaseLLMConnector):
    def __init__(self, model=MODEL_LLAMA, system_prompt=ASISTANT_SYSTEM_PROMPT):
        super().__init__(model, system_prompt)

        self.connector = ollama

    def _prepare_messages(self):
        default_messages = [{"role": "system", "content": self.system_prompt}]
        messages = []

        if self._is_single_ask_mode_enabled and not self._is_conversation_mode_enabled:
            messages = default_messages + [{"role": "user", "content": self._question}]
        
        if not self._is_single_ask_mode_enabled and self._is_conversation_mode_enabled:
            messages = default_messages + self._messages

        return messages

    def _get_connector_response(self):
        messages = self._prepare_messages()

        return self.connector.chat(
            model=self.model,
            messages=messages
        )

    def _parse_response(self, response):
        return response['message']['content']
    
    def _create_stream(self):
        messages = self._prepare_messages()
        
        return self.connector.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )

    def _parse_stream_chunk(self, chunk):
        return chunk['message']['content']