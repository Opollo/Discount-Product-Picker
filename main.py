from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx

app = FastAPI(title="AI Discount & Product Assistant")

# 🌍 Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧭 Redirect root to your frontend (GitHub Pages)
@app.get("/", include_in_schema=False)
def redirect_to_frontend():
    return RedirectResponse(url="https://opollo.github.io/discount-picker/")

# 🩺 Health check route
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# 🛒 Mock data for demonstration
SAMPLE_DEALS = {
    "amazon": [
        {"name": "Bluetooth Headphones", "price": 49, "original_price": 70, "discount": "30%"},
        {"name": "Smart Watch", "price": 79, "original_price": 100, "discount": "21%"},
    ],
    "alibaba": [
        {"name": "Wireless Mouse", "price": 10, "original_price": 20, "discount": "50%"},
        {"name": "USB-C Charger", "price": 15, "original_price": 25, "discount": "40%"},
    ],
    "jumia": [
        {"name": "Phone Case", "price": 15, "original_price": 25, "discount": "40%"},
        {"name": "Screen Protector", "price": 5, "original_price": 10, "discount": "50%"},
    ]
}

# 🔍 Universal deals route
@app.get("/api/deals")
def get_discounts(platform: str = Query(None, description="Platform name: amazon, alibaba, jumia")):
    if platform is None:
        all_deals = []
        for deals in SAMPLE_DEALS.values():
            all_deals.extend(deals)
        return {"platform": "all", "deals": all_deals}

    platform = platform.lower()
    if platform not in SAMPLE_DEALS:
        raise HTTPException(status_code=404, detail=f"No deals found for platform '{platform}'")

    return {"platform": platform, "deals": SAMPLE_DEALS[platform]}

# 🔎 Simulate product search per platform
@app.get("/api/search/{platform}")
async def search_products(platform: str, query: str):
    platform = platform.lower()
    if platform not in SAMPLE_DEALS:
        raise HTTPException(status_code=404, detail=f"Platform '{platform}' not supported.")

    # Simple mock filtering
    results = [
        deal for deal in SAMPLE_DEALS[platform]
        if query.lower() in deal["name"].lower()
    ]
    return {"platform": platform, "results": results or SAMPLE_DEALS[platform]}

# 🧠 AI Chat route that powers the chatbot in index.html
@app.get("/api/chat")
async def chat_ai(q: str):
    q_lower = q.lower()
    response = {"query": q, "response": "", "deals": []}

    # Detect platform keywords
    if "amazon" in q_lower:
        response["response"] = "Here are some current deals from Amazon:"
        response["deals"] = SAMPLE_DEALS["amazon"]
    elif "alibaba" in q_lower:
        response["response"] = "These are trending items on Alibaba:"
        response["deals"] = SAMPLE_DEALS["alibaba"]
    elif "jumia" in q_lower:
        response["response"] = "Jumia discounts available now:"
        response["deals"] = SAMPLE_DEALS["jumia"]
    elif "trend" in q_lower:
        response["response"] = "Here’s a simple market trend: electronics and smart devices are rising in popularity."
    elif "cheap" in q_lower or "discount" in q_lower:
        response["response"] = "Here are current hot deals across all stores:"
        all_deals = []
        for deals in SAMPLE_DEALS.values():
            all_deals.extend(deals)
        response["deals"] = all_deals
    else:
        response["response"] = (
            "I can help you find discounts on Amazon, Alibaba, or Jumia. "
            "Try asking: 'Show Amazon deals on smart watches.'"
        )

    return response
