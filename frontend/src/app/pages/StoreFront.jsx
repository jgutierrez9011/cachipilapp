import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getProducts, getStore } from '../api/public'
import { useCartStore } from '../state/cartStore'

export default function StoreFront() {
  const { slug } = useParams()
  const [store, setStore] = useState(null)
  const [products, setProducts] = useState([])
  const [error, setError] = useState('')
  const { items, add, subtotal } = useCartStore()

  useEffect(() => {
    Promise.all([getStore(slug), getProducts(slug)])
      .then(([storeRes, productsRes]) => {
        setStore(storeRes)
        setProducts(productsRes)
      })
      .catch((err) => setError(err.message))
  }, [slug])

  return (
    <main style={{ maxWidth: 800, margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>{store?.name || 'Tienda'}</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {products.map((product) => (
          <li key={product.id} style={{ marginBottom: 12 }}>
            <strong>{product.name}</strong> - C${Number(product.price).toFixed(2)}
            <button onClick={() => add(product)} style={{ marginLeft: 10 }}>
              Agregar
            </button>
          </li>
        ))}
      </ul>

      <section>
        <h3>Carrito ({items.length})</h3>
        <p>Subtotal: C${subtotal().toFixed(2)}</p>
        <Link to={`/t/${slug}/checkout`}>Ir al checkout</Link>
      </section>
    </main>
  )
}
