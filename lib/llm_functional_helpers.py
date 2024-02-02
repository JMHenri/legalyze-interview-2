from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from datetime import datetime

class ReceiptItem(BaseModel):
    item_name: str = Field(..., description="Name of the item purchased")
    item_price: str = Field(..., description="Price of the item before tax")
    item_price_with_tax: str = Field(..., description="Price of the item after tax")
    item_purchase_date: str = Field(..., description="Date when the item was purchased")

    # Custom validation to ensure the date is correctly formatted
    @validator("item_purchase_date")
    def validate_date_format(cls, v):
        try:
            # Attempt to parse the date to ensure it's valid
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("item_purchase_date must be in YYYY-MM-DD format")

    # You might also want to validate the item price and item price with tax to ensure they are in a proper numeric format.
    # Add custom validators here if needed.


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