from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
import json

logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """Abstract base class for all AI models in Kakhoot."""
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        pass

class OpenAIModel(BaseModel):
    """Wrapper for OpenAI models."""
    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("Please install the openai package: pip install openai")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_name = model_name
        logger.info(f"Initialized OpenAIModel with model: {self.model_name}")

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        try:
            completion_params = {
                "model": self.model_name,
                "messages": messages,
                **kwargs
            }
            if tools:
                completion_params["tools"] = tools
                completion_params["tool_choice"] = "auto"

            response = await self.client.chat.completions.create(**completion_params)
            
            content = response.choices[0].message.content
            tool_calls = response.choices[0].message.tool_calls
            
            result = {"content": content}
            if tool_calls:
                result["tool_calls"] = [{
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    },
                    "id": tc.id # Include tool_call_id for OpenAI
                } for tc in tool_calls]
                result["raw_tool_calls"] = tool_calls # Store raw tool calls for agent to use
            return result
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return {"content": f"Error: {e}"}

class AnthropicModel(BaseModel):
    """Wrapper for Anthropic models."""
    def __init__(self, api_key: str, model_name: str = "claude-3-opus-20240229"):
        try:
            from anthropic import AsyncAnthropic
        except ImportError:
            raise ImportError("Please install the anthropic package: pip install anthropic")
        self.client = AsyncAnthropic(api_key=api_key)
        self.model_name = model_name
        logger.info(f"Initialized AnthropicModel with model: {self.model_name}")

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        try:
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Anthropic expects system message at the top level, not in messages list
                    kwargs["system"] = msg["content"]
                else:
                    anthropic_messages.append(msg)

            completion_params = {
                "model": self.model_name,
                "max_tokens": 4096, # Anthropic requires max_tokens
                "messages": anthropic_messages,
                **kwargs
            }
            if tools:
                completion_params["tools"] = tools

            response = await self.client.messages.create(**completion_params)
            
            content = ""
            tool_calls = []
            raw_tool_calls = []

            for block in response.content:
                if block.type == "text":
                    content += block.text
                elif block.type == "tool_use":
                    tool_calls.append({
                        "function": {
                            "name": block.name,
                            "arguments": json.dumps(block.input)
                        },
                        "id": block.id
                    })
                    raw_tool_calls.append(block) # Store raw tool calls
            
            result = {"content": content.strip()}
            if tool_calls:
                result["tool_calls"] = tool_calls
                result["raw_tool_calls"] = raw_tool_calls
            return result
        except Exception as e:
            logger.error(f"Anthropic API Error: {e}")
            return {"content": f"Error: {e}"}

class LocalModel(BaseModel):
    """Placeholder for local models (e.g., Ollama, Hugging Face local inference)."""
    def __init__(self, model_path: str = "mock_local_model", **kwargs):
        self.model_path = model_path
        logger.info(f"Initialized LocalModel from: {model_path}")
        # In a real scenario, you would load your local model here
        # e.g., using transformers library or an Ollama client

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        logger.debug(f"Local Model received messages: {messages}")
        
        # Simple mock logic for local model to simulate tool calls or content generation
        last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

        # Simple mock logic for local model to simulate tool calls or content generation
        # Check if the last message was a tool output
        last_msg = messages[-1]
        if last_msg["role"] == "tool":
            return {"content": f"I processed the tool output: {last_msg['content']}"}

        last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

        if tools and "call_tool" in last_user_message.lower():
            # Simulate a tool call based on a keyword in the message
            mock_tool_name = "mock_tool"
            mock_tool_args = {"query": last_user_message.replace("call_tool", "").strip()}
            mock_tool_id = "call_mock_tool_123"

            # Find a matching tool in the provided schema
            for tool_schema in tools:
                if tool_schema["function"]["name"] == mock_tool_name:
                    logger.info(f"LocalModel simulating tool call: {mock_tool_name}")
                    return {
                        "content": f"I need to use a tool to answer this.",
                        "tool_calls": [{
                            "function": {
                                "name": mock_tool_name,
                                "arguments": json.dumps(mock_tool_args)
                            },
                            "id": mock_tool_id
                        }],
                        "raw_tool_calls": [{"id": mock_tool_id, "type": "tool_use", "name": mock_tool_name, "input": mock_tool_args}]
                    }
            logger.warning(f"LocalModel couldn't find mock_tool in provided schema: {tools}")
            return {"content": f"Local model tried to call a tool but couldn't find it: {last_user_message}"}
        
        response_content = f"Local model processed: {last_user_message}"
        return {"content": response_content}
