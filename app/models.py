from pydantic import BaseModel, HttpUrl, root_validator, Field
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

class Product(BaseModel):
    id: str
    title: str
    vendor: str
    original_price: Decimal = Field(..., gt=Decimal("0"))
    current_price: Decimal = Field(..., ge=Decimal("0"))
    discount_pct: Decimal = Field(None, ge=Decimal("0"), le=Decimal("100"))
    url: HttpUrl
    image: Optional[HttpUrl] = None
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @root_validator(pre=True)
    def compute_discount(cls, values):
        # Ensure Decimal conversion for prices
        op = values.get("original_price")
        cp = values.get("current_price")
        # allow strings/floats; convert to Decimal
        try:
            if op is not None:
                values["original_price"] = Decimal(str(op))
            if cp is not None:
                values["current_price"] = Decimal(str(cp))
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid price format")

        op = values.get("original_price")
        cp = values.get("current_price")
        if op is not None and cp is not None and op > 0:
            discount = (op - cp) / op * Decimal("100")
            # normalize to 2 decimal places
            values["discount_pct"] = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            values["discount_pct"] = Decimal("0.00")
        # Ensure last_seen is timezone-aware UTC
        ls = values.get("last_seen")
        if ls is None:
            values["last_seen"] = datetime.now(timezone.utc)
        elif ls.tzinfo is None:
            values["last_seen"] = ls.replace(tzinfo=timezone.utc)
        return values
