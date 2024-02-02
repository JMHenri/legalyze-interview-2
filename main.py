from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from lib.text_processing import parse_fulltext_receipt_data
from lib.llm_functional_helpers import format_openai_receipt_response
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.runnables import RunnableParallel



OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')


# Read the text data from the file
with open('data.txt', 'r') as file:
    text_data = file.read()
# Parse the data into individual receipts
parsed_data = parse_fulltext_receipt_data(text_data)


# Create a ChatOpenAI instance
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
llm_with_tools = llm.bind_tools([format_openai_receipt_response], tool_choice="format_openai_receipt_response")


receipt_chains = {}
for i, data in enumerate(parsed_data, start=1):
    chain_key = f'receiptChain{i}'
    receipt_chains[chain_key] = ChatPromptTemplate.from_messages([
        ("system", "Please parse the given receipt so that it is usable in the provided function."),
        ("user", data)
    ]) | llm_with_tools

map_chain = RunnableParallel(**receipt_chains)

res = map_chain.invoke({"input": ''})

# Print the result
print(res)

