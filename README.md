# 🚀 Kakhoot: The Minimalist AI Orchestration Framework

![Kakhoot Status](https://img.shields.io/badge/Status-Alpha-orange) ![License](https://img.shields.io/badge/License-MIT-blue) ![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)

**Kakhoot** is a high-performance, minimalist AI orchestration framework designed for developers who want to build autonomous agents with plug-and-play model support without the complexity of larger frameworks. Focus on your agent's logic, and let Kakhoot handle the rest.

## ✨ Features

- **Plug-and-Play Models**: Easily integrate with OpenAI, Anthropic, and local models (e.g., Ollama, Hugging Face) with a unified API.
- **Intuitive Tool Calling**: Define and register tools with simple decorators, allowing your agents to interact with external systems.
- **Autonomous Agent Loop**: A built-in conversational loop for agents to reason, act, and refine their responses.
- **Lightweight & Fast**: Designed for performance and a smooth developer experience.
- **Extensible**: Easily add new models, tools, and agent behaviors.
- **CLI Interface**: Interact with your agents directly from the command line.

## ⚡ Quick Start

### 1. Installation

```bash
pip install kakhoot
```

Alternatively, clone the repository and install:

```bash
git clone https://github.com/adeniyisogo/kakhoot.git
cd kakhoot
pip install -e .
```

### 2. Define Your Tools

Create a Python file (e.g., `my_tools.py`):

```python
from kakhoot.core import Tool

@Tool(name="get_current_weather", description="Get the current weather in a given location")
def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location."""
    # In a real application, this would call an external weather API
    return f"The weather in {location} is 72 degrees {unit} and sunny."

@Tool(name="get_n_day_forecast", description="Get the N-day forecast for a given location")
def get_n_day_forecast(location: str, num_days: int) -> str:
    """Get the N-day forecast for the next N days in a given location."""
    # In a real application, this would call an external weather API
    return f"The {num_days}-day forecast for {location} is mostly sunny with a chance of pixel rain."
```

### 3. Create Your Agent

```python
import os
from kakhoot.core import Agent
from kakhoot.models import OpenAIModel
from my_tools import get_current_weather, get_n_day_forecast # Import your tools

# Initialize your model (e.g., OpenAI)
# Ensure OPENAI_API_KEY is set in your environment variables or .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your environment or .env file.")

model = OpenAIModel(api_key=openai_api_key)

# Create an agent and register your tools
agent = Agent(model=model, tools=[get_current_weather, get_n_day_forecast])

# Run the agent with an initial message
async def main():
    response = await agent.run("What's the weather like in San Francisco?")
    print(f"Agent Response: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 4. Run from CLI

```bash
# Using OpenAI model
kakhoot --model openai --api-key YOUR_OPENAI_API_KEY --message "What's the 3-day forecast for London?"

# Using a local model (mocked for now)
kakhoot --model local --local-model-path /path/to/your/local/model --message "Tell me a story."
```

## 📚 Documentation

- **`kakhoot/core.py`**: Defines the `Agent` class and `Tool` decorator for creating intelligent agents and their capabilities.
- **`kakhoot/models.py`**: Provides a unified interface for various AI models (OpenAI, Anthropic, Local).
- **`kakhoot/cli.py`**: Command-line interface for interacting with Kakhoot agents.
- **`setup.py`**: Package configuration for easy installation.

## 🛠️ Development

### Project Structure

```
kakhoot/
├── kakhoot/
│   ├── __init__.py         # Package initialization
│   ├── core.py             # Agent and Tool definitions
│   ├── models.py           # Model interfaces (OpenAI, Anthropic, Local)
│   └── cli.py              # Command-line interface
├── setup.py                # Package setup file
├── README.md               # Project documentation
├── LICENSE                 # MIT License
└── .gitignore              # Git ignore file
```

### Running Tests (Coming Soon)

```bash
pytest
```

## 🤝 Contributing

We welcome contributions to make Kakhoot even better! Please see `CONTRIBUTING.md` for guidelines.

### Ideas for Contributions

- **New Model Integrations**: Add support for more LLM providers (e.g., Google Gemini, Cohere).
- **Advanced Tooling**: Implement more sophisticated tool parameter parsing (e.g., Pydantic validation).
- **Agent Orchestration**: Add support for multi-agent systems and complex workflows.
- **CLI Enhancements**: Improve the CLI with more features and a richer user experience.
- **Examples & Tutorials**: Provide more diverse examples and detailed tutorials.
- **Performance Optimizations**: Further enhance the speed and efficiency of the framework.

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for simpler, more flexible AI agent development.
- Built with the open-source community in mind.

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/adeniyisogo/kakhoot/issues)

---

**Made with ❤️ by Manus AI for the open-source community**

⭐ If you find Kakhoot useful, please consider giving it a star on GitHub! ⭐
