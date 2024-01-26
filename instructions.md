Create a function that uses RAG to fetch context from the example.txt document. The main task is to parse data from the receipts and output it in a structured json string dynamically with Langchain.

Format to be used:
```json
{
    "data": [
        { 
            "item_name": "iPhone 14 Pro",
            "item_price": "999.00",
            "item_price_with_tax": "1073.93",
            "item_purchase_date": "2024-01-26"
        },
        {
            "item_name": "MacBook Pro",
            "item_price": "1299.00",
            "item_price_with_tax": "1402.92",
            "item_purchase_date": "2024-01-26"
        },
        {
            "item_name": "AirPods Pro",
            "item_price": "249.00",
            "item_price_with_tax": "266.43",
            "item_purchase_date": "2024-01-26"
        }
    ]
}
```