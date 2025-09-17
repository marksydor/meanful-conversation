from openai import OpenAI

from classes.base_llm_connector import BaseLLMConnector
from constants.default import ASISTANT_SYSTEM_PROMPT, MODEL_GPT

class OpenAIConnector(BaseLLMConnector):
    def __init__(self, model=MODEL_GPT, system_prompt=ASISTANT_SYSTEM_PROMPT, api_key=None):
        super().__init__(model, system_prompt)

        if not api_key or not api_key.startswith("sk-proj-") or len(api_key) < 10:
            raise PermissionError("There might be a problem with your API key")

        self.connector = OpenAI(api_key=api_key)

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
        
        return self.connector.chat.completions.create(
            model=self.model,
            messages=messages
        )

    def _parse_response(self, response):
        return response.choices[0].message.content

    def _create_stream(self):
        messages = self._prepare_messages()

        return self.connector.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

    def _parse_stream_chunk(self, chunk):
        return chunk.choices[0].delta.content