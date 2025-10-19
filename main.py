from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to the Discount Product Picker API. Use /discounts to get deals."}
