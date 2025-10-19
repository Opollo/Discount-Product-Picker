import os

async def get_amazon_deals():
    api_key = os.getenv("AMAZON_API_KEY")
    return [{
        "platform": "Amazon",
        "title": "Wireless Headphones",
        "original_price": 100.0,
        "discounted_price": 45.0,
        "discount_percentage": 55,
        "url": "https://www.amazon.com/dp/example",
        "image": "https://example.com/image.jpg"
    }]