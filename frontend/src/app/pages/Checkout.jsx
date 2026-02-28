import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { createOrder } from '../api/public'
import { useCartStore } from '../state/cartStore'

export default function Checkout() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { items, subtotal, clear } = useCartStore()
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    customer_name: '',
    customer_whatsapp: '',
    delivery_method: 'DELIVERY',
    address_text: '',
    notes: '',
    payment_method: 'CASH',
    delivery_fee: 0,
  })

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (items.length === 0) return setError('El carrito está vacío')
    if (form.delivery_method === 'DELIVERY' && !form.address_text.trim()) return setError('La dirección es requerida para delivery')

    try {
      const payload = {
        ...form,
        store_slug: slug,
        delivery_fee: Number(form.delivery_fee || 0),
        items: items.map((it) => ({ product_id: it.product_id, qty: it.qty })),
      }
      const res = await createOrder(payload)
      clear()
      window.location.href = res.whatsapp_url
      navigate(`/t/${slug}/order-created`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h2>Checkout</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={onSubmit}>
        <input placeholder="Nombre" value={form.customer_name} onChange={(e) => setForm({ ...form, customer_name: e.target.value })} />
        <input placeholder="WhatsApp" value={form.customer_whatsapp} onChange={(e) => setForm({ ...form, customer_whatsapp: e.target.value })} />
        <select value={form.delivery_method} onChange={(e) => setForm({ ...form, delivery_method: e.target.value })}>
          <option value="DELIVERY">Delivery</option>
          <option value="PICKUP">Pickup</option>
        </select>
        {form.delivery_method === 'DELIVERY' && (
          <input placeholder="Dirección" value={form.address_text} onChange={(e) => setForm({ ...form, address_text: e.target.value })} />
        )}
        <input placeholder="Notas" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <select value={form.payment_method} onChange={(e) => setForm({ ...form, payment_method: e.target.value })}>
          <option value="CASH">Efectivo</option>
          <option value="TRANSFER">Transferencia</option>
          <option value="CARD_LINK">Link tarjeta</option>
        </select>
        <input type="number" step="0.01" placeholder="Envío C$" value={form.delivery_fee} onChange={(e) => setForm({ ...form, delivery_fee: e.target.value })} />
        <p>Subtotal: C${subtotal().toFixed(2)}</p>
        <button type="submit">Confirmar pedido</button>
      </form>
    </main>
  )
}
