from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.models.store import Store
from app.schemas.order import OrderCreateIn, OrderCreateOut
from app.schemas.product import ProductPublicOut
from app.schemas.store import StorePublicOut
from app.services.orders_service import create_order

router = APIRouter(prefix='/public', tags=['public'])


@router.get('/stores/{slug}', response_model=StorePublicOut)
def get_store(slug: str, db: Session = Depends(get_db)) -> Store:
    store = db.scalar(select(Store).where(Store.slug == slug, Store.is_active.is_(True)))
    if not store:
        raise HTTPException(status_code=404, detail='Store not found')
    return store


@router.get('/stores/{slug}/products', response_model=list[ProductPublicOut])
def list_products(slug: str, db: Session = Depends(get_db)) -> list[Product]:
    store = db.scalar(select(Store).where(Store.slug == slug, Store.is_active.is_(True)))
    if not store:
        raise HTTPException(status_code=404, detail='Store not found')

    products = db.scalars(
        select(Product).where(Product.store_id == store.id, Product.is_active.is_(True)).order_by(Product.created_at.desc())
    ).all()
    return list(products)


@router.post('/orders', response_model=OrderCreateOut)
def create_public_order(payload: OrderCreateIn, db: Session = Depends(get_db)) -> OrderCreateOut:
    return create_order(db, payload)
