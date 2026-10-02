from dotenv import load_dotenv
from openai import OpenAI
import json

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

tool_call = response.output[0]

arguments = json.loads(tool_call.arguments)

weather_result = get_weather(arguments["location"])

final_response = client.responses.create(
    model="gpt-5.4-nano",
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": weather_result
        }
    ]
)

print(final_response.output_text)