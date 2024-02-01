from lib.text_processing import parse_receipt_data

# Read the text data from the file
with open('data.txt', 'r') as file:
    text_data = file.read()

# Parse the data
parsed_data = parse_receipt_data(text_data)
