import os

async def get_jumia_deals():
    api_key = os.getenv("JUMIA_API_KEY")
    return [{
        "platform": "Jumia",
        "title": "LED TV 32-inch",
        "original_price": 250.0,
        "discounted_price": 120.0,
        "discount_percentage": 52,
        "url": "https://www.jumia.ug/product/example",
        "image": "https://example.com/image3.jpg"
    }]