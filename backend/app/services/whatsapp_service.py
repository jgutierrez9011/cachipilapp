from decimal import Decimal
from urllib.parse import quote

from app.models.order import Order, OrderItem


def currency(value: Decimal) -> str:
    return f'C${value:.2f}'


def build_whatsapp_message(order: Order, customer_name: str, customer_whatsapp: str, items: list[OrderItem]) -> str:
    lines = [
        f'Pedido #{order.public_code}',
        f'Cliente: {customer_name}',
        f'WhatsApp: {customer_whatsapp}',
        f'Entrega: {order.delivery_method.value}',
    ]
    if order.delivery_method.value == 'DELIVERY' and order.address_text:
        lines.append(f'Dirección: {order.address_text}')
    lines.append('Productos:')

    for item in items:
        lines.append(f'- {item.qty} x {item.name_snapshot} = {currency(item.line_total)}')

    lines.extend(
        [
            f'Subtotal: {currency(order.subtotal)}',
            f'Envío: {currency(order.delivery_fee)}',
            f'Total: {currency(order.total)}',
            f'Pago: {order.payment_method.value}',
            'Gracias por tu pedido 🙌',
        ]
    )
    return '\n'.join(lines)


def build_whatsapp_url(store_whatsapp_e164: str, message: str) -> str:
    return f'https://wa.me/{store_whatsapp_e164}?text={quote(message)}'
