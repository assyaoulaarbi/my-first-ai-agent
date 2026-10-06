from dotenv import load_dotenv
from openai import OpenAI
import json

# 1. Load API key
load_dotenv()

# 2. Our actual Python tool
def get_weather(location):
    return f"The weather in {location} is sunny and 75°F."

def add_numbers(a, b):
    return a + b

# 3. Connect to OpenAI
client = OpenAI()

# 4. Describe our tools to the LLM
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
    },
    {
        "type": "function",
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number"
                },
                "b": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["a", "b"]
        }
    }
]

# 5. Our LLM request
response = client.responses.create(
    model="gpt-5.4-nano",
    input="What is the weather in Paris?",
    tools=tools
)

tool_call = response.output[0]

print("Tool chosen:", tool_call.name)
print("Arguments chosen:", tool_call.arguments)

arguments = json.loads(tool_call.arguments)

if tool_call.name == "get_weather":
    tool_result = get_weather(arguments["location"])

elif tool_call.name == "add_numbers":
    tool_result = add_numbers(arguments["a"], arguments["b"])

print("Tool result:", tool_result)

final_response = client.responses.create(
    model="gpt-5.4-nano",
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(tool_result)
        }
    ]
)

print("Final answer:", final_response.output_text)
