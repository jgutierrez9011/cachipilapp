from decimal import Decimal

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.product import Product
from app.models.store import Store


def run_seed() -> None:
    db = SessionLocal()
    try:
        store = db.scalar(select(Store).where(Store.slug == 'demo'))
        if not store:
            store = Store(name='Demo Store', slug='demo', whatsapp_e164='50588889999')
            db.add(store)
            db.flush()

        existing = db.scalars(select(Product).where(Product.store_id == store.id)).all()
        if existing:
            print('Seed ya aplicado')
            db.commit()
            return

        products = [
            Product(store_id=store.id, name='Quesillo', price=Decimal('60.00'), stock_qty=30, is_active=True),
            Product(store_id=store.id, name='Torta de tres leches', price=Decimal('120.00'), stock_qty=15, is_active=True),
            Product(store_id=store.id, name='Café helado', price=Decimal('85.00'), stock_qty=20, is_active=True),
            Product(store_id=store.id, name='Empanada de pollo', price=Decimal('45.00'), stock_qty=50, is_active=True),
            Product(store_id=store.id, name='Batido de fresa', price=Decimal('95.00'), stock_qty=25, is_active=True),
        ]
        db.add_all(products)
        db.commit()
        print('Seed aplicado correctamente')
    finally:
        db.close()


if __name__ == '__main__':
    run_seed()
