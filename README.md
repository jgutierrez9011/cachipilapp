# Cachipilapp - Multi-store WhatsApp Commerce (MVP)

Plataforma multi-negocio tipo catálogo + carrito + pedidos por WhatsApp.

## Requisitos
- Docker + Docker Compose
- (Sin Docker) Python 3.12+, Node 20+, PostgreSQL 16+

## Levantar con Docker Compose
```bash
docker compose up --build
```

Backend: http://localhost:8000
Frontend: http://localhost:5173

### Migraciones y seed
```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed
```

## Ejecutar sin Docker
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Endpoints públicos
- `GET /health`
- `GET /public/stores/{slug}`
- `GET /public/stores/{slug}/products`
- `POST /public/orders`

## Flujo WhatsApp
1. Cliente arma carrito en `/t/:slug`.
2. Checkout envía orden a `POST /public/orders`.
3. Backend guarda orden y devuelve `whatsapp_url`.
4. Frontend redirige a WhatsApp (`wa.me`) con mensaje prellenado.

## Ejemplo curl crear orden
```bash
curl -X POST http://localhost:8000/public/orders \
  -H "Content-Type: application/json" \
  -d '{
    "store_slug": "demo",
    "customer_name": "Ana Perez",
    "customer_whatsapp": "88889999",
    "delivery_method": "DELIVERY",
    "address_text": "Semáforos del mayoreo 1c al sur",
    "notes": "Sin cebolla",
    "payment_method": "CASH",
    "delivery_fee": 40,
    "items": [
      {"product_id": "00000000-0000-0000-0000-000000000000", "qty": 2}
    ]
  }'
```
