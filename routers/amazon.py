from fastapi import APIRouter
from services.fetch_amazon import get_amazon_deals

router = APIRouter(prefix="/api/deals/amazon", tags=["Amazon"])

@router.get("/")
async def fetch_amazon_deals():
    return await get_amazon_deals()