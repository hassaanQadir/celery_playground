import time
import asyncio
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from molbio import create_llmchain

# Load environment variables
load_dotenv('.env')

# Use the environment variables for the API keys if available
openai_api_key = os.getenv('OPENAI_API_KEY')

async def async_generate(chain, answer):
    resp = await chain.arun({'text': "Make glow in the dark E. coli"})
    answer.append(resp)

async def generate_concurrently():
    chain = create_llmchain(1)
    answer = []
    tasks = [async_generate(chain, answer) for _ in range(20)]
    await asyncio.gather(*tasks)
    return answer

list1 = asyncio.run(generate_concurrently())
print(list1)