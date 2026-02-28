from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.order import DeliveryMethod, PaymentMethod


class OrderItemIn(BaseModel):
    product_id: UUID
    qty: int = Field(gt=0)


class OrderCreateIn(BaseModel):
    store_slug: str = Field(min_length=2, max_length=120)
    customer_name: str = Field(min_length=2, max_length=255)
    customer_whatsapp: str
    delivery_method: DeliveryMethod
    address_text: str | None = None
    notes: str | None = None
    payment_method: PaymentMethod
    delivery_fee: Decimal = Field(default=0, ge=0)
    items: list[OrderItemIn]

    @field_validator('store_slug')
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator('items')
    @classmethod
    def validate_items_not_empty(cls, value: list[OrderItemIn]) -> list[OrderItemIn]:
        if not value:
            raise ValueError('items no puede estar vacío')
        return value

    @model_validator(mode='after')
    def validate_delivery_address(self):
        if self.delivery_method == DeliveryMethod.DELIVERY and not self.address_text:
            raise ValueError('address_text es requerido para DELIVERY')
        return self


class OrderCreateOut(BaseModel):
    public_code: str
    whatsapp_message: str
    whatsapp_url: str
    subtotal: Decimal
    delivery_fee: Decimal
    total: Decimal
