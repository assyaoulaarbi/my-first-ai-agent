from dotenv import load_dotenv
from openai import OpenAI

# 1. Load API key
load_dotenv()

# 2. Our actual Python tool
def get_weather(location):
    return f"The weather in {location} is sunny and 75°F."

# 3. Connect to OpenAI
client = OpenAI()

# 4. Describe our tool to the LLM
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city to get weather for"
                }
            },
            "required": ["location"]
        }
    }
]

# 5. Our LLM request
response = client.responses.create(
    model="gpt-5.4-nano",
    input="What is the weather in Dallas?",
    tools=tools
)

print(response.output)