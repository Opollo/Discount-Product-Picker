from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers import amazon, alibaba, jumia

app = FastAPI(title="Discount Product Picker AI")

# 🔁 Redirect root to frontend
@app.get("/", include_in_schema=False)
def redirect_to_frontend():
    return RedirectResponse(url="https://opollo.github.io/discount-picker/")  # Replace with your frontend URL

# 🛡️ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧩 Include routers
app.include_router(amazon.router)
app.include_router(alibaba.router)
app.include_router(jumia.router)

# 💓 Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# 🛍️ Sample deals per platform
SAMPLE_DEALS = {
    "amazon": [
        {"name": "Bluetooth Headphones", "price": 49, "original_price": 70},
        {"name": "Smart Watch", "price": 79, "original_price": 100},
    ],
    "alibaba": [
        {"name": "Wireless Mouse", "price": 10, "original_price": 20},
        {"name": "USB-C Charger", "price": 15, "original_price": 25},
    ],
    "jumia": [
        {"name": "Phone Case", "price": 15, "original_price": 25},
        {"name": "Screen Protector", "price": 5, "original_price": 10},
    ]
}

# 🔎 Discounts route with platform filter
@app.get("/discounts")
def get_discounts(platform: str = None):
    if platform is None:
        # Return all deals if no platform is specified
        all_deals = []
        for deals in SAMPLE_DEALS.values():
            all_deals.extend(deals)
        return all_deals

    platform = platform.lower()
    if platform not in SAMPLE_DEALS:
        raise HTTPException(status_code=404, detail=f"No deals found for platform '{platform}'")

    return SAMPLE_DEALS[platform]
