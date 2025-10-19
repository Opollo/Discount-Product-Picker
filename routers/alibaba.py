from fastapi import APIRouter
from services.fetch_alibaba import get_alibaba_deals

router = APIRouter(prefix="/api/deals/alibaba", tags=["Alibaba"])

@router.get("/")
async def fetch_alibaba_deals():
    return await get_alibaba_deals()