import openai
from dotenv import load_dotenv
import os
from openai_multi_client import OpenAIMultiOrderedClient

# Load environment variables
load_dotenv('.env')

# Use the environment variables for the API keys if available
openai.api_key = os.getenv('OPENAI_API_KEY')

# Remember to set the OPENAI_API_KEY environment variable to your API key
api = OpenAIMultiOrderedClient(endpoint="chats", data_template={"model": "gpt-3.5-turbo"})

def make_requests():
    for num in range(1, 10):
        api.request(data={
            "messages": [{
                "role": "user",
                "content": f"Can you tell me what is {num} * {num}? Incorporate the answer into a joke?"
            }]
        }, metadata={'num': num})


api.run_request_function(make_requests)

for result in api:
    num = result.metadata['num']
    response = result.response['choices'][0]['message']['content']
    print(f"{num} * {num}:", response)