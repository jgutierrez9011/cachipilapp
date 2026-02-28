import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = (UniqueConstraint('store_id', 'whatsapp_e164', name='uq_customer_store_whatsapp'),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)
    whatsapp_e164: Mapped[str] = mapped_column(String(20), nullable=False)
    name_last: Mapped[str | None] = mapped_column(String(140))
    total_orders: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_order_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
