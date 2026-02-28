import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProductImage(Base):
    __tablename__ = 'product_images'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
