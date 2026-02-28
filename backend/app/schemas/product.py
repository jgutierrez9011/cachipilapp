from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductPublicOut(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    stock_qty: int | None
