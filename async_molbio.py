import time
import json
import itertools
import asyncio
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from molbio import create_llmchain, askOpenTrons

# Load environment variables
load_dotenv('.env')

# Use the environment variables for the API keys if available
openai_api_key = os.getenv('OPENAI_API_KEY')

async def async_generate(chain, prompt):
    resp = await chain.arun({'text': prompt})
    return resp

async def generate_concurrently(chain, inputList):
    tasks = [async_generate(chain, input) for input in inputList]
    outputList = await asyncio.gather(*tasks)
    return outputList

def process_results(rawList):
    allCleanedItems = []
    for item in rawList:
        rawItems = item.split('|||')
        newCleanedItems = [s for s in rawItems if len(s) >= 10]
        allCleanedItems.extend(newCleanedItems)

    return allCleanedItems

def applyLayer(chain, inputList):
    rawList = asyncio.run(generate_concurrently(chain, inputList))
    finalList = process_results(rawList)
    return finalList


def displayOutput(list1, list2, list3, list4):
    nested_dict = {}

    for l1 in list1:
        nested_dict[l1] = {}
        for l2 in list2[:3]:
            nested_dict[l1][l2] = {}
            for l3 in list3[:8]:
                nested_dict[l1][l2][l3] = list(itertools.islice(list4, 0, 3))
                del list4[:3]
            del list3[:8]
        del list2[:3]

    return nested_dict

def driver(user_input):
    user_input = [user_input]
    outputData = {}
    print("we've entered the driver")

    #here we create the chains
    chain1 = create_llmchain(1)
    chain2 = create_llmchain(2)
    chain3 = create_llmchain(3)
    chain4 = create_llmchain(4)
    print("chains created")
    
    #here we run each layer, which is multiple concurrent requests to a given chain
    layer1 = applyLayer(chain1, user_input)
    layer2 = applyLayer(chain2, layer1)
    layer3 = applyLayer(chain3, layer2)
    layer4 = applyLayer(chain4, layer3)
    print("layer 4 done")
    
    # now that we've created all the output,
    # we pass it to a function which puts it in a nested dictionary to print out to display it
    outputData = displayOutput(layer1, layer2, layer3, layer4)
    print(json.dumps(outputData, indent=4))

    return outputData

driver("Make yeast that can detect equol")