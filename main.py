from dotenv import load_dotenv
load_dotenv()
import os
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from lib.text_processing import parse_fulltext_receipt_data
from lib.llm_functional_helpers import format_openai_receipt_response
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.runnables import RunnableParallel
from langchain.output_parsers import PydanticOutputParser


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


# Initialize a list to hold the parsed data
parsed_items = []

for chain_key, ai_message in res.items():
    tool_calls = ai_message.additional_kwargs.get('tool_calls', [])
    for call in tool_calls:
        function_info = call.get('function', {})
        arguments_json = function_info.get('arguments', '{}')
        arguments_dict = json.loads(arguments_json)
        
        # Date formatting
        item_purchase_date = arguments_dict.get("item_purchase_date", "")
        formatted_date = datetime.strptime(item_purchase_date, "%B %d, %Y").strftime("%Y-%m-%d")
        
        # Dictionary ordering and formatting
        item_data = {
            "item_name": arguments_dict.get("item_name", ""),
            "item_price": arguments_dict.get("item_price", "").replace("$", ""),  # Remove dollar sign
            "item_price_with_tax": arguments_dict.get("item_price_with_tax", "").replace("$", ""),  # Remove dollar sign
            "item_purchase_date": formatted_date
        }
        parsed_items.append(item_data)


final_structure = {
    "data": parsed_items
}
json_output = json.dumps(final_structure, indent=4)

print(json_output)