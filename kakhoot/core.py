import inspect
import json
from typing import Callable, Dict, Any, List, Optional

class Tool:
    """Decorator to register a function as a tool for the Agent."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __call__(self, func: Callable) -> Callable:
        func._is_tool = True
        func._tool_name = self.name
        func._tool_description = self.description
        func._tool_parameters = self._extract_parameters(func)
        return func

    def _extract_parameters(self, func: Callable) -> Dict[str, Any]:
        signature = inspect.signature(func)
        parameters = {}
        for name, param in signature.parameters.items():
            if name == 'self':  # Skip 'self' for methods
                continue
            param_type = str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any'
            parameters[name] = {"type": param_type, "description": f"Parameter {name}"}
            # TODO: Add more sophisticated description extraction (e.g., from docstrings)
        return parameters

def register_tool(name: str, description: str) -> Callable:
    """Function to register a tool, alternative to decorator."""
    return Tool(name, description)

class Agent:
    """Base class for an AI agent in Kakhoot."""
    def __init__(self, model: Any, tools: Optional[List[Callable]] = None):
        self.model = model
        self._registered_tools: Dict[str, Callable] = {}
        if tools:
            for tool_func in tools:
                self.add_tool(tool_func)

    def add_tool(self, tool_func: Callable):
        """Adds a tool function to the agent."""
        if not hasattr(tool_func, '_is_tool') or not tool_func._is_tool:
            raise ValueError(f"Function {tool_func.__name__} is not a registered tool. Use @Tool decorator or register_tool.")
        self._registered_tools[tool_func._tool_name] = tool_func

    def get_tool_schema(self) -> List[Dict[str, Any]]:
        """Returns the JSON schema for all registered tools."""
        schema = []
        for tool_name, tool_func in self._registered_tools.items():
            schema.append({
                "type": "function",
                "function": {
                    "name": tool_func._tool_name,
                    "description": tool_func._tool_description,
                    "parameters": {
                        "type": "object",
                        "properties": tool_func._tool_parameters,
                        "required": [name for name, param in inspect.signature(tool_func).parameters.items() if param.default == inspect.Parameter.empty and name != 'self']
                    }
                }
            })
        return schema

    async def chat(self, message: str, **kwargs) -> Any:
        """Sends a message to the model and handles tool calls."""
        messages = [{"role": "user", "content": message}]
        tools_schema = self.get_tool_schema()

        response = await self.model.generate(messages, tools=tools_schema, **kwargs)
        
        # Basic tool calling logic (can be expanded)
        if response and response.get("tool_calls"):
            tool_calls = response["tool_calls"]
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                
                if tool_name in self._registered_tools:
                    tool_func = self._registered_tools[tool_name]
                    print(f"\n>>> Calling tool: {tool_name} with args: {tool_args}")
                    tool_output = tool_func(**tool_args)
                    print(f"<<< Tool output: {tool_output}")
                    # You would typically feed this output back to the model
                    # For simplicity, we'll just return the output for now
                    return tool_output
                else:
                    print(f"Tool {tool_name} not found.")
            
        return response.get("content", "No response or tool call.")

    async def run(self, initial_message: str, max_iterations: int = 5, **kwargs) -> Any:
        """Runs the agent in a loop, handling tool calls and responses."""
        current_message = initial_message
        for i in range(max_iterations):
            print(f"\n--- Agent Iteration {i+1} ---")
            print(f"User message: {current_message}")
            response = await self.chat(current_message, **kwargs)
            
            if isinstance(response, str) and response.startswith("No response or tool call."):
                print("Agent finished without further tool calls.")
                return response
            elif response is not None:
                # Assuming tool_output is the response if a tool was called
                current_message = f"Tool output: {response}"
            else:
                print("Agent finished.")
                return response
        print("Max iterations reached.")
        return "Max iterations reached without a clear conclusion."
