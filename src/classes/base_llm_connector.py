from abc import ABC, abstractmethod
import types

class BaseLLMConnector(ABC):
    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt
        self.on_stream_event = None        
        self.last_result = None

        self._is_single_ask_mode_enabled = False
        self._is_conversation_mode_enabled = False
        self._messages = []
        self._question = None
        self._run_method = self._run_default
        self._is_stream_in_process = False
        self._stream = None
        self._is_printing_enabled = False
        
    def reset(self):
        self._question = None
        self.last_result = None
        self._run_method = self._run_default
        self._is_stream_in_process = False
        self._stream = None
        self._is_printing_enabled = False
        self.on_stream_event = None
        self._messages = []
    
    def ask(self, question: str):
        self._is_single_ask_mode_enabled = True
        self._is_conversation_mode_enabled = False
        self._question = question
        return self
    
    def conversation(self, messages: list):
        self._is_single_ask_mode_enabled = False
        self._is_conversation_mode_enabled = True
        self._messages = messages
        return self
    
    def set_model(self, model: str):
        self.model = model
        return self

    def get_result(self):
        return self.last_result
    
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        return self

    def print_result(self):
        if self.last_result is None:
            raise ValueError("No result to print_result. Call run() first.")
        else:
            print(self.last_result)
        return self
        
    def stream(self):
        if not self._run_stream:
            raise RuntimeError("No stream processor set. Call set_stream_runner(fn) first.")
        self._run_method = self._run_stream
        return self

    def set_stream_runner(self, fn):
        self._run_stream = fn
        return self

    def enable_print_result(self):
        self._is_printing_enabled = True
        return self

    def set_on_stream_event(self, on_stream_event):
        self.on_stream_event = on_stream_event
        return self
    
    @abstractmethod
    def _get_connector_response(self):
        pass
    
    @abstractmethod
    def _parse_response(self, response):
        pass
    
    @abstractmethod
    def _create_stream(self):
        pass

    @abstractmethod
    def _parse_stream_chunk(self, chunk):
        pass

    def _stream_wrapper(self, stream):
        for event in stream:
            chunk = self._parse_stream_chunk(event)
            if chunk:
                yield chunk
            elif chunk in {"message.error", "message.stopped", "error"}:
                print("Error during stream")
                break
    
    def _process_stream_response(self, stream):
        self.last_result = ""
        parts = []
        
        try:
            for chunk in self._stream_wrapper(stream):
                
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
        
    def _run_default(self):
        response = self._get_connector_response()
        
        parsed_response = self._parse_response(response)

        self.last_result = parsed_response

        return self

    
    def _run_stream(self):
        self._stream = self._create_stream()
        self._is_stream_in_process = True
        self._process_stream_response(self._stream)
        
        return self

    def run(self):
        self._run_method()
        return self
