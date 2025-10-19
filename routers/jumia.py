from fastapi import APIRouter
from services.fetch_jumia import get_jumia_deals

router = APIRouter(prefix="/api/deals/jumia", tags=["Jumia"])

@router.get("/")
async def fetch_jumia_deals():
    return await get_jumia_deals()