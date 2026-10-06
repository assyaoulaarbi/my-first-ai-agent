from dotenv import load_dotenv
from openai import OpenAI
import json

# 1. Load API key
load_dotenv()

# 2. Our actual Python tools
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


# 5. Create the conversation input
input_list = [
    {
        "role": "user",
        "content": "What is the weather in Dallas, and what is 27 + 58?"
    }
]


# 6. Ask the LLM what tools it needs
response = client.responses.create(
    model="gpt-5.4-nano",
    input=input_list,
    tools=tools
)


# 7. Keep the LLM's output in the conversation
input_list += response.output


# 8. Execute every tool requested by the LLM
for tool_call in response.output:

    # Ignore anything that is not a function call
    if tool_call.type != "function_call":
        continue

    arguments = json.loads(tool_call.arguments)

    print("Tool chosen:", tool_call.name)
    print("Arguments chosen:", tool_call.arguments)
    print("Call ID:", tool_call.call_id)

    if tool_call.name == "get_weather":
        tool_result = get_weather(arguments["location"])

    elif tool_call.name == "add_numbers":
        tool_result = add_numbers(
            arguments["a"],
            arguments["b"]
        )

    else:
        raise ValueError(f"Unknown tool: {tool_call.name}")

    print("Tool result:", tool_result)

    # Add this tool's result to the conversation
    input_list.append(
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(tool_result)
        }
    )


# 9. Send all tool results back to the LLM
final_response = client.responses.create(
    model="gpt-5.4-nano",
    input=input_list,
    tools=tools
)


# 10. Print the final answer
print("Final answer:", final_response.output_text)