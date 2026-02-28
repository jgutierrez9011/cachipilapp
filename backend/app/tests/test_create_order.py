

def test_create_order_success(client):
    products = client.get('/public/stores/demo/products').json()
    product_id = products[0]['id']

    payload = {
        'store_slug': 'demo',
        'customer_name': 'Ana Perez',
        'customer_whatsapp': '88889999',
        'delivery_method': 'DELIVERY',
        'address_text': 'Managua Centro',
        'notes': 'Sin cebolla',
        'payment_method': 'CASH',
        'delivery_fee': '40.00',
        'items': [{'product_id': product_id, 'qty': 2}],
    }

    response = client.post('/public/orders', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['public_code']
    assert body['total'] == '160.00'
    assert body['whatsapp_url'].startswith('https://wa.me/50588889999?text=')
