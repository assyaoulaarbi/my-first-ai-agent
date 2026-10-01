from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4-nano",
    input="Say: Hello Assya, your first AI API call works!"
)

print(response.output_text)
