from langchain.decorators import llm_function

@llm_function
def format_receipt_data(item_name: str, item_price: str, item_price_with_tax: str, item_purchase_date: str):
    """
    Formats receipt data into a structured JSON format using OpenAI.

    Args:
        item_name (str): Name of the item.
        item_price (str): Price of the item.
        item_price_with_tax (str): Price of the item including tax.
        item_purchase_date (str): Purchase date of the item.

    Returns:
        dict: A dictionary representing the structured data of the item.
    """
    return {
        "item_name": item_name,
        "item_price": item_price,
        "item_price_with_tax": item_price_with_tax,
        "item_purchase_date": item_purchase_date
    }



@llm_prompt
def parse_receipt(receipt:str, functions:List[Union[Callable,BaseTool]]):
    """ 
    ``` <prompt:system>
    Your role is to be a helpful asistant. Parse the information provided in the receipt to match the
    data format for the provided function.
    ```
    ``` <prompt:user>
    {receipt}
    ```
    """

result = parse_receipt(
        receipt=receipt, 
        functions=[format_receipt_data]
    )

if result.is_function_call:
    result.execute()
else:
    print(result.output_text)