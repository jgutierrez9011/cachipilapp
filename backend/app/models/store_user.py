import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StoreUser(Base):
    __tablename__ = 'store_users'
    __table_args__ = (UniqueConstraint('store_id', 'email', name='uq_store_users_store_email'),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
