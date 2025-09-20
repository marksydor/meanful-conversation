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

    def is_tool_run_needed(self, response) -> bool:
        return response.message.tool_calls is not None and len(response.message.tool_calls) > 0

    def is_stream_tool_run_needed(self, event) -> bool: 
        return event['message'].get('tool_calls') is not None and len(event['message']['tool_calls']) > 0

    def _get_tool_name(self, response) -> str:
        return response.message.tool_calls[0].function.name

    def _get_tool_args(self, response, tool_name: str) -> dict:
        for tool_call in response.message.tool_calls:
            if tool_call.function.name == tool_name:
                return tool_call.function.arguments
        return {}

    def _return_tool_results_back_to_llm(self, tool_results) -> dict:
        for tool_result in tool_results:
            self._messages.append({"role": "tool", "name": tool_result["name"], "content": str(tool_result["result"])})
        return self.run()

    def _get_tool_names_list(self, response) -> list:
        names = []
        for tool_call in response.message.tool_calls:
            names.append(tool_call.function.name)
        return names 
       

    def _get_connector_response(self):
        messages = self._prepare_messages()

        tools = self._prepare_tools()

        return self.connector.chat(
            model=self.model,
            messages=messages,
            tools=tools if self.is_tools_available else None,
        )

    def _parse_response(self, response):
        return response['message']['content']
    
    def _create_stream(self):
        messages = self._prepare_messages()

        tools = self._prepare_tools()

        return self.connector.chat(
            model=self.model,
            messages=messages,
            tools=tools if self.is_tools_available else None,
            stream=True,
        )

    def _parse_response(self, response):
        return response['message']['content']

    def _parse_stream_chunk(self, chunk):
        return chunk['message']['content']
    
    