"""
from abc import ABC, abstractmethod
from typing import List
from httpx import AsyncClient
from app.models import Product

class BaseFetcher(ABC):
    """
    Fetcher interface accepts an AsyncClient so we reuse connections/timeouts.
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    @abstractmethod
    async def fetch(self) -> List[Product]:
        raise NotImplementedError
"""