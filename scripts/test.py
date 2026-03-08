from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),  # or GSK_API_KEY if that's your var
    base_url="https://api.x.ai/v1",
)

models = client.models.list()

print("Available models:\n")
for m in models.data:
    print(m.id)