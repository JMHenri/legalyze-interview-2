import re

def parse_receipt_data(text):
    # Split the text into individual receipts, removing empty strings resulting from split
    receipts = [receipt.strip() for receipt in text.strip().split('============================================') if receipt.strip()]

    # Array to store the string representation of each receipt
    receipt_strings = []

    for receipt in receipts:
        # Add the entire receipt as a single string to the list
        receipt_strings.append(receipt)

    return receipt_strings
