from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to the Discount Product Picker API. Use /discounts to get deals."}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)
