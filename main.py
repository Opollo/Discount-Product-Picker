from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

# 🔁 Redirect root to your frontend
@app.get("/", include_in_schema=False)
def redirect_to_frontend():
    return RedirectResponse(url="https://opollo.github.io/discount-picker/")  # Replace with your actual frontend URL

# 🛡️ Enable CORS so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain for security
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛍️ Your actual API route
@app.get("/discounts")
def get_discounts():
    # Your logic to fetch and return discounted products
    return [{"platform": "Amazon", "name": "Sample Product", "price": 25, "original_price": 50}]
