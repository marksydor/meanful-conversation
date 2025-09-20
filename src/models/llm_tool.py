from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Dict

@dataclass
class LLMTool:
    # Required fields
    type: str = field(default="function")   # has default value
    name: str = field(default_factory=str)  # must be provided
    executer: Callable[..., Any] = field(default=None)  # must be provided
    description: str = field(default_factory=str)     # must be provided
    
    # Optional fields
    parameters: Optional[Dict[str, Any]] = None

    def execute(self, *args, **kwargs) -> Any:
        if not callable(self.executer):
            raise ValueError(f"Executer for tool '{self.name}' is not callable.")
        return self.executer(*args, **kwargs)

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters or {"type": "object", "properties": {}}
            }
        }