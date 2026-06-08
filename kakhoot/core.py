import inspect
import json
from typing import Callable, Dict, Any, List, Optional, Type, get_origin, get_args
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Mapping Python types to JSON schema types
PYTHON_TO_JSON_TYPES = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
}

def get_json_type(py_type: Type) -> str:
    """Converts a Python type to its JSON schema equivalent."""
    origin = get_origin(py_type)
    if origin is list:
        return "array"
    elif origin is dict:
        return "object"
    elif origin is Optional:
        # Handle Optional[X] by getting the inner type
        args = get_args(py_type)
        if args:
            return get_json_type(args[0])
    return PYTHON_TO_JSON_TYPES.get(py_type, "string") # Default to string

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
        properties = {}
        required_params = []

        # Extract docstring for parameter descriptions
        doc = inspect.getdoc(func)
        param_docs = {}
        if doc:
            in_args_section = False
            for line in doc.split("\n"): 
                stripped_line = line.strip()
                if stripped_line.startswith("Args:"):
                    in_args_section = True
                    continue
                if in_args_section and stripped_line and stripped_line[0].isalpha() and not stripped_line.startswith(" "): # Check if it's a new section
                    in_args_section = False
                if in_args_section and ":" in stripped_line:
                    try:
                        # Split by first colon to handle type hints like `param (str):`
                        parts = stripped_line.split(":", 1)
                        param_name_and_type = parts[0].strip()
                        param_desc = parts[1].strip()
                        
                        # Extract just the parameter name (e.g., from "location (str)")
                        param_name = param_name_and_type.split()[0]
                        param_docs[param_name] = param_desc
                    except ValueError:
                        pass

        for name, param in signature.parameters.items():
            if name == 'self':  # Skip 'self' for methods
                continue

            param_type = param.annotation
            json_type = get_json_type(param_type)
            
            param_info = {
                "type": json_type,
                "description": param_docs.get(name, f"Parameter {name}")
            }
            properties[name] = param_info

            if param.default == inspect.Parameter.empty:
                required_params.append(name)
        
        return {"type": "object", "properties": properties, "required": required_params}

def register_tool(name: str, description: str) -> Callable:
    """Function to register a tool, alternative to decorator."""
    return Tool(name, description)

class Agent:
    """Base class for an AI agent in Kakhoot."""
    def __init__(self, model: Any, tools: Optional[List[Callable]] = None, system_prompt: Optional[str] = None):
        self.model = model
        self.system_prompt = system_prompt
        self._registered_tools: Dict[str, Callable] = {}
        if tools:
            for tool_func in tools:
                self.add_tool(tool_func)

    def add_tool(self, tool_func: Callable):
        """Adds a tool function to the agent."""
        if not hasattr(tool_func, '_is_tool') or not tool_func._is_tool:
            raise ValueError(f"Function {tool_func.__name__} is not a registered tool. Use @Tool decorator or register_tool.")
        self._registered_tools[tool_func._tool_name] = tool_func
        logger.debug(f"Registered tool: {tool_func._tool_name}")

    def get_tool_schema(self) -> List[Dict[str, Any]]:
        """Returns the JSON schema for all registered tools."""
        schema = []
        for tool_name, tool_func in self._registered_tools.items():
            schema.append({
                "type": "function",
                "function": {
                    "name": tool_func._tool_name,
                    "description": tool_func._tool_description,
                    "parameters": tool_func._tool_parameters
                }
            })
        return schema

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Sends messages to the model and handles tool calls."""
        tools_schema = self.get_tool_schema()
        # Only pass tools if there are registered tools
        if tools_schema:
            response = await self.model.generate(messages, tools=tools_schema, **kwargs)
        else:
            response = await self.model.generate(messages, **kwargs)
        return response

    async def run(self, initial_message: str, max_iterations: int = 10, **kwargs) -> Any:
        """Runs the agent in a loop, handling tool calls and responses."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
            
        messages.append({"role": "user", "content": initial_message})
        
        for i in range(max_iterations):
            logger.info(f"--- Agent Iteration {i+1} ---")
            
            # Print the last message added to the context
            last_msg = messages[-1]
            if last_msg["role"] == "user":
                logger.info(f"User: {last_msg['content']}")
            elif last_msg["role"] == "tool":
                logger.info(f"Tool Output ({last_msg.get('name', 'unknown')}): {last_msg['content']}")

            response = await self.chat(messages, **kwargs)
            
            if response.get("tool_calls"):
                tool_calls = response["tool_calls"]
                
                # Append the assistant's message containing the tool calls to the history
                assistant_message = {"role": "assistant", "content": response.get("content", "")}
                if "raw_tool_calls" in response:
                    # If the model provides raw tool calls (like OpenAI), append them
                    assistant_message["tool_calls"] = response["raw_tool_calls"]
                messages.append(assistant_message)

                for tool_call in tool_calls:
                    tool_name = tool_call["function"]["name"]
                    try:
                        tool_args = json.loads(tool_call["function"]["arguments"])
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse arguments for tool {tool_name}: {tool_call['function']['arguments']}")
                        tool_args = {}
                    
                    if tool_name in self._registered_tools:
                        tool_func = self._registered_tools[tool_name]
                        logger.info(f">>> Calling tool: {tool_name} with args: {tool_args}")
                        try:
                            tool_output = tool_func(**tool_args)
                            logger.info(f"<<< Tool output: {tool_output}")
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.get("id", "mock_id"), # Required for OpenAI
                                "name": tool_name,
                                "content": str(tool_output)
                            })
                        except Exception as e:
                            error_message = f"Error executing tool {tool_name}: {e}"
                            logger.error(error_message)
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.get("id", "mock_id"),
                                "name": tool_name,
                                "content": error_message
                            })
                    else:
                        error_message = f"Tool {tool_name} not found."
                        logger.warning(error_message)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.get("id", "mock_id"),
                            "name": tool_name,
                            "content": error_message
                        })
                # Loop continues to let the model process the tool output
            elif response.get("content"):
                content = response["content"]
                logger.info(f"Agent: {content}")
                messages.append({"role": "assistant", "content": content})
                return content # Agent has a final text response
            else:
                logger.warning("Agent finished without a clear response or tool call.")
                return "Agent finished without a clear response or tool call."
        
        logger.warning("Max iterations reached.")
        return "Max iterations reached without a clear conclusion."
