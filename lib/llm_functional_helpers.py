def format_openai_receipt_response(item_name: str, item_price: str, item_price_with_tax: str, item_purchase_date: str):
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