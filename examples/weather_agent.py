import os
import asyncio
from kakhoot.core import Agent, Tool
from kakhoot.models import OpenAIModel, AnthropicModel, LocalModel

# 1. Define your tools using the @Tool decorator
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
    # 2. Choose and initialize your model
    # For this example, we'll use OpenAI. Make sure OPENAI_API_KEY is set.
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY not found. Using a mock local model for demonstration.")
        model = LocalModel(model_path="mock_path")
    else:
        model = OpenAIModel(api_key=openai_api_key)

    # 3. Create an agent and register your tools
    agent = Agent(model=model, tools=[get_current_weather, get_n_day_forecast])

    print("\n--- Running Agent with a simple query ---")
    response1 = await agent.run("What is the weather like in San Francisco?")
    print(f"Agent Response 1: {response1}")

    print("\n--- Running Agent with a forecast query ---")
    response2 = await agent.run("What's the 3-day forecast for London in Celsius?")
    print(f"Agent Response 2: {response2}")

    print("\n--- Running Agent with an unknown location ---")
    response3 = await agent.run("What's the weather in Paris?")
    print(f"Agent Response 3: {response3}")

if __name__ == "__main__":
    # To run this example, ensure you have the required packages installed:
    # pip install kakhoot openai python-dotenv
    # And set your OPENAI_API_KEY environment variable.
    asyncio.run(main())
