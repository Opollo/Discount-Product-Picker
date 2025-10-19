from fastapi import APIRouter, Query, Depends, Request
from typing import List, Optional
from app.models import Product
from app.services.aggregator import Aggregator
from httpx import AsyncClient

router = APIRouter(prefix="/deals", tags=["deals"])

async def get_http_client(request: Request) -> AsyncClient:
    """
    Dependency to retrieve the shared AsyncClient created in app startup.
    """
    return request.app.state.http_client

@router.get("", response_model=List[Product])
async def list_deals(
    min_discount: float = Query(50.0, ge=0.0, le=100.0, description="Minimum discount percentage to include"),
    vendor: Optional[str] = Query(None, description="Optional vendor filter (e.g. 'jumia', 'amazon')"),
    client: AsyncClient = Depends(get_http_client),
):
    """
    Return aggregated deals across configured vendors with at least min_discount.
    """
    aggregator = Aggregator(client=client)
    deals = await aggregator.get_deals(min_discount=min_discount, vendor=vendor)
    return deals
