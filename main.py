from fastapi import FastAPI
<<<<<<< HEAD
from routers import amazon, alibaba, jumia

app = FastAPI(title="Discount Product Picker AI")

app.include_router(amazon.router)
app.include_router(alibaba.router)
app.include_router(jumia.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
=======
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
>>>>>>> 0e060a24a96597d666806035d03df7dfd2f6c18c
