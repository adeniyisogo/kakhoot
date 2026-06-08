import argparse
import asyncio
import os
from kakhoot.core import Agent, Tool
from kakhoot.models import OpenAIModel, AnthropicModel, LocalModel

# Example tools for demonstration
@Tool(name="get_current_weather", description="Get the current weather in a given location")
def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 72 degrees {unit} and sunny."

@Tool(name="get_n_day_forecast", description="Get the N-day forecast for a given location")
def get_n_day_forecast(location: str, num_days: int) -> str:
    """Get the N-day forecast for a given location."""
    return f"The {num_days}-day forecast for {location} is mostly sunny."

async def main():
    parser = argparse.ArgumentParser(description="Kakhoot AI Agent CLI")
    parser.add_argument("--model", type=str, default="openai", help="Model to use (openai, anthropic, local)")
    parser.add_argument("--api-key", type=str, help="API key for the model (if required)")
    parser.add_argument("--message", type=str, required=True, help="Message to send to the agent")
    parser.add_argument("--max-iterations", type=int, default=5, help="Maximum iterations for agent run")
    parser.add_argument("--local-model-path", type=str, help="Path to local model for local backend")

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
        if not args.local_model_path:
            print("Error: --local-model-path is required for local model.")
            return
        model = LocalModel(model_path=args.local_model_path)
    else:
        print(f"Error: Unknown model type: {args.model}")
        return

    if model:
        agent = Agent(model=model, tools=[get_current_weather, get_n_day_forecast])
        result = await agent.run(initial_message=args.message, max_iterations=args.max_iterations)
        print("\n--- Agent Final Result ---")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
