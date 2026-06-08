import argparse
import asyncio
import os
from kakhoot.core import Agent, Tool
from kakhoot.models import OpenAIModel, AnthropicModel, LocalModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example tools for demonstration
@Tool(name="get_current_weather", description="Get the current weather in a given location")
def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.

    Args:
        location (str): The city and state, e.g., San Francisco, CA
        unit (str): The unit of temperature, can be 'celsius' or 'fahrenheit'. Defaults to 'fahrenheit'.
    """
    # In a real application, this would call an external weather API
    if "tokyo" in location.lower():
        return "The weather in Tokyo is 15 degrees Celsius and cloudy."
    elif "san francisco" in location.lower():
        return "The weather in San Francisco is 68 degrees Fahrenheit and sunny."
    elif "london" in location.lower():
        return "The weather in London is 10 degrees Celsius and rainy."
    else:
        return f"Weather data for {location} not available."

@Tool(name="get_n_day_forecast", description="Get the N-day forecast for a given location")
def get_n_day_forecast(location: str, num_days: int) -> str:
    """Get the N-day forecast for the next N days in a given location.

    Args:
        location (str): The city and state, e.g., San Francisco, CA
        num_days (int): The number of days to get the forecast for.
    """
    # In a real application, this would call an external weather API
    if "tokyo" in location.lower():
        return f"The {num_days}-day forecast for Tokyo is mostly cloudy with occasional showers."
    elif "san francisco" in location.lower():
        return f"The {num_days}-day forecast for San Francisco is mostly sunny with cool mornings."
    elif "london" in location.lower():
        return f"The {num_days}-day forecast for London is rainy and chilly."
    else:
        return f"Forecast data for {location} not available."

async def main():
    parser = argparse.ArgumentParser(description="Kakhoot AI Agent CLI")
    parser.add_argument("--model", type=str, default="openai", help="Model to use (openai, anthropic, local)")
    parser.add_argument("--api-key", type=str, help="API key for the model (if required)")
    parser.add_argument("--message", type=str, required=True, help="Message to send to the agent")
    parser.add_argument("--max-iterations", type=int, default=10, help="Maximum iterations for agent run")
    parser.add_argument("--local-model-path", type=str, default="mock_path", help="Path to local model for local backend")
    parser.add_argument("--system-prompt", type=str, help="System prompt for the agent")

    args = parser.parse_args()

    model = None
    if args.model == "openai":
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OpenAI API key not provided. Use --api-key or set OPENAI_API_KEY environment variable.")
            return
        model = OpenAIModel(api_key=api_key)
    elif args.model == "anthropic":
        api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: Anthropic API key not provided. Use --api-key or set ANTHROPIC_API_KEY environment variable.")
            return
        model = AnthropicModel(api_key=api_key)
    elif args.model == "local":
        model = LocalModel(model_path=args.local_model_path)
    else:
        print(f"Error: Unknown model type: {args.model}")
        return

    if model:
        agent = Agent(model=model, tools=[get_current_weather, get_n_day_forecast], system_prompt=args.system_prompt)
        result = await agent.run(initial_message=args.message, max_iterations=args.max_iterations)
        print("\n--- Agent Final Result ---")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
