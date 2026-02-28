from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import DeliveryMethod, Order, OrderItem
from app.models.product import Product
from app.models.store import Store
from app.schemas.order import OrderCreateIn, OrderCreateOut
from app.services.whatsapp_service import build_whatsapp_message, build_whatsapp_url
from app.utils.codes import generate_public_code
from app.utils.validation import normalize_nicaragua_whatsapp


def _get_unique_code(db: Session, store_id) -> str:
    for _ in range(15):
        code = generate_public_code()
        existing = db.scalar(select(Order).where(Order.store_id == store_id, Order.public_code == code))
        if not existing:
            return code
    raise HTTPException(status_code=500, detail='No se pudo generar código de orden único')


def create_order(db: Session, payload: OrderCreateIn) -> OrderCreateOut:
    store = db.scalar(select(Store).where(Store.slug == payload.store_slug, Store.is_active.is_(True)))
    if not store:
        raise HTTPException(status_code=404, detail='Tienda no encontrada')

    if payload.delivery_method == DeliveryMethod.DELIVERY and not payload.address_text:
        raise HTTPException(status_code=400, detail='address_text es requerido para DELIVERY')

    normalized_wa = normalize_nicaragua_whatsapp(payload.customer_whatsapp)

    customer = db.scalar(
        select(Customer).where(Customer.store_id == store.id, Customer.whatsapp_e164 == normalized_wa)
    )
    if not customer:
        customer = Customer(store_id=store.id, name_last=payload.customer_name, whatsapp_e164=normalized_wa)
        db.add(customer)
        db.flush()
    else:
        customer.name_last = payload.customer_name

    product_ids = [item.product_id for item in payload.items]
    products = db.scalars(
        select(Product).where(
            Product.store_id == store.id,
            Product.is_active.is_(True),
            Product.id.in_(product_ids),
        )
    ).all()
    products_by_id = {product.id: product for product in products}

    if len(products_by_id) != len(set(product_ids)):
        raise HTTPException(status_code=400, detail='Hay productos inválidos o inactivos en el pedido')

    subtotal = Decimal('0')
    order_items: list[OrderItem] = []

    for item in payload.items:
        product = products_by_id[item.product_id]
        if product.stock_qty is not None and item.qty > product.stock_qty:
            raise HTTPException(status_code=400, detail=f'Sin stock suficiente para {product.name}')

        line_total = Decimal(product.price) * item.qty
        subtotal += line_total

        order_items.append(
            OrderItem(
                product_id=product.id,
                name_snapshot=product.name,
                price_snapshot=product.price,
                qty=item.qty,
                line_total=line_total,
            )
        )

    total = subtotal + payload.delivery_fee
    order = Order(
        store_id=store.id,
        customer_id=customer.id,
        public_code=_get_unique_code(db, store.id),
        delivery_method=payload.delivery_method,
        address_text=payload.address_text,
        notes=payload.notes,
        payment_method=payload.payment_method,
        customer_name=payload.customer_name,
        customer_whatsapp=normalized_wa,
        subtotal=subtotal,
        delivery_fee=payload.delivery_fee,
        total=total,
        whatsapp_message='',
    )
    order.items = order_items
    db.add(order)
    db.flush()

    message = build_whatsapp_message(order, payload.customer_name, normalized_wa, order_items)
    order.whatsapp_message = message
    customer.total_orders += 1
    customer.last_order_at = order.created_at
    db.commit()

    return OrderCreateOut(
        public_code=order.public_code,
        whatsapp_message=message,
        whatsapp_url=build_whatsapp_url(store.whatsapp_e164, message),
        subtotal=subtotal,
        delivery_fee=payload.delivery_fee,
        total=total,
    )
