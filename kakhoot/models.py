from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        try:
            if tools:
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    **kwargs
                )
            else:
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    **kwargs
                )
            
            # Extracting content and tool calls
            content = response.choices[0].message.content
            tool_calls = response.choices[0].message.tool_calls
            
            result = {"content": content}
            if tool_calls:
                result["tool_calls"] = [{
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in tool_calls]
            return result
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return {"content": f"Error: {e}"}

class AnthropicModel(BaseModel):
    """Wrapper for Anthropic models."""
    def __init__(self, api_key: str, model_name: str = "claude-3-opus-20240229"):
        try:
            from anthropic import Anthropic, AsyncAnthropic
        except ImportError:
            raise ImportError("Please install the anthropic package: pip install anthropic")
        self.client = AsyncAnthropic(api_key=api_key)
        self.model_name = model_name

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        try:
            # Anthropic tools integration is different, requires specific formatting
            # For simplicity, this example will focus on basic message generation
            # Full tool support would require more complex message formatting for Anthropic
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                messages=messages,
                **kwargs
            )
            return {"content": response.content[0].text}
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            return {"content": f"Error: {e}"}

class LocalModel(BaseModel):
    """Placeholder for local models (e.g., Ollama, Hugging Face local inference)."""
    def __init__(self, model_path: str, **kwargs):
        self.model_path = model_path
        print(f"Initializing local model from: {model_path}")
        # In a real scenario, you would load your local model here
        # e.g., using transformers library or an Ollama client

    async def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, **kwargs) -> Dict[str, Any]:
        # This is a mock implementation for a local model
        print(f"Local Model received messages: {messages}")
        if tools:
            print(f"Local Model received tools: {tools}")
            # Simulate tool call if a specific message pattern is detected
            for message in messages:
                if "call_tool" in message["content"].lower():
                    # Mock a tool call response
                    return {
                        "tool_calls": [{
                            "function": {
                                "name": "mock_tool",
                                "arguments": "{\"param1\": \"value1\"}"
                            }
                        }],
                        "content": "I think I need to use a tool."
                    }
        
        last_message = messages[-1]["content"]
        response_content = f"Local model processed: 
{last_message}"
        return {"content": response_content}
