from fastapi import FastAPI
from routers import amazon, alibaba, jumia

app = FastAPI(title="Discount Product Picker AI")

app.include_router(amazon.router)
app.include_router(alibaba.router)
app.include_router(jumia.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}