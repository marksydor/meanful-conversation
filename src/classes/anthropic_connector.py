import anthropic

from classes.base_llm_connector import BaseLLMConnector
from constants.default import ASISTANT_SYSTEM_PROMPT, MODEL_ANTHROPIC
import types

class AnthropicConnector(BaseLLMConnector):
    def __init__(self, model=MODEL_ANTHROPIC, system_prompt=ASISTANT_SYSTEM_PROMPT, api_key=None, max_tokens=1024):
        super().__init__(model, system_prompt)

        if not api_key:
            raise PermissionError("API key is required for AnthropicConnector")

        self.max_tokens = max_tokens
        self.connector = anthropic.Anthropic(api_key=api_key)

    def set_max_tokens(self, max_tokens: int):
        self.max_tokens = max_tokens
        return self

    def _prepare_messages(self):
        messages = []

        if self._is_single_ask_mode_enabled and not self._is_conversation_mode_enabled:
            messages = [{"role": "user", "content": self._question}]

        if not self._is_single_ask_mode_enabled and self._is_conversation_mode_enabled:
            messages = self._messages

        return messages

    def _get_connector_response(self):
        messages = self._prepare_messages()

        return self.connector.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            system=self.system_prompt,
        )

    def _parse_response(self, response):
        return response.content[0].text

    def _create_stream(self):
        messages = self._prepare_messages()

        stream_manager = self.connector.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            system=self.system_prompt,
        )

        return stream_manager

    def _process_stream_response(self, stream_manager):
        self.last_result = ""
        parts = []
        
        try:
            with stream_manager as stream:
                for chunk in stream.text_stream:            
                    cleaned = chunk.replace("```", "")
                    parts.append(cleaned)
                
                    self.last_result = "".join(parts)
                
                    if self._is_printing_enabled:
                        print(cleaned, end='', flush=True)
                    
                    if self.on_stream_event and isinstance(self.on_stream_event, types.FunctionType):
                        self.on_stream_event(chunk)
                    
            return self.last_result
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self._is_stream_in_process = False


    def _parse_stream_chunk(self, chunk):
        print("Anthropic stream chunk:", chunk)
        return chunk