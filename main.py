from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import uvicorn

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated product database
PRODUCTS = [
    {"name": "Samsung Galaxy A14", "price": "$180", "store": "Amazon"},
    {"name": "Infinix Smart 7", "price": "$95", "store": "Jumia"},
    {"name": "HP Pavilion Laptop", "price": "$620", "store": "Alibaba"},
    {"name": "Noise Cancelling Headphones", "price": "$120", "store": "Amazon"},
    {"name": "Solar Power Bank", "price": "$35", "store": "Jumia"},
]

@app.get("/search")
def search(query: str):
    results = [p for p in PRODUCTS if query.lower() in p["name"].lower()]
    return JSONResponse(content={"products": results})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
