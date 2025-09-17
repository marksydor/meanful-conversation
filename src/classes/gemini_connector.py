
from google import genai
from google.genai import types

from classes.base_llm_connector import BaseLLMConnector
from constants.default import ASISTANT_SYSTEM_PROMPT, MODEL_GEMINI

class GeminiConnector(BaseLLMConnector):
    def __init__(self, model=MODEL_GEMINI, system_prompt=ASISTANT_SYSTEM_PROMPT, api_key=None):
        super().__init__(model, system_prompt)

        if not api_key:
            raise PermissionError("API key is required for GeminiConnector")

        self.connector = genai.Client(api_key=api_key)

    @staticmethod
    def _normalize_role(role: str) -> str:
        if not role:
            return "user"
        r = role.lower()
        if r in ("assistant", "asistant"):
            return "model"
        if r == "model":
            return "model"
        if r == "system":
            return "system"
        return "user"


    def _to_genai_contents(self, messages):

        contents = []
        
        for m in messages:
            role = self._normalize_role(m.get("role", "user"))
            
            text = m.get("content") if isinstance(m.get("content"), str) else str(m.get("content"))
            
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=text)]
                )
            )
        return contents

    def _prepare_messages(self):
        messages = []

        if self._is_single_ask_mode_enabled and not self._is_conversation_mode_enabled:
            messages = [{"role": "user", "content": self._question}]

        if not self._is_single_ask_mode_enabled and self._is_conversation_mode_enabled:
            messages = list(self._messages)

        return messages

    def _get_connector_response(self):
        messages = self._prepare_messages()

        contents = self._to_genai_contents(messages)
        
        response = self.connector.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
        )
        return response

    def _parse_response(self, response):
        return getattr(response, "text", None)
    
    def _create_stream(self):
        messages = self._prepare_messages()

        contents = self._to_genai_contents(messages)


        stream = self.connector.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
        )

        return stream

    def _parse_stream_chunk(self, chunk):
        return getattr(chunk, "text", None)