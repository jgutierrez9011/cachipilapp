from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.product import Product
from app.models.store import Store


@pytest.fixture()
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestingSessionLocal() as db:
        store = Store(name='Demo Store', slug='demo', whatsapp_e164='50588889999', is_active=True)
        db.add(store)
        db.flush()
        db.add(
            Product(
                store_id=store.id,
                name='Quesillo',
                price=Decimal('60.00'),
                stock_qty=10,
                is_active=True,
            )
        )
        db.commit()

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
