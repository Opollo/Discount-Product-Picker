import os

async def get_alibaba_deals():
    api_key = os.getenv("ALIBABA_API_KEY")
    return [{
        "platform": "Alibaba",
        "title": "Smartwatch Series X",
        "original_price": 80.0,
        "discounted_price": 35.0,
        "discount_percentage": 56,
        "url": "https://www.alibaba.com/product/example",
        "image": "https://example.com/image2.jpg"
    }]