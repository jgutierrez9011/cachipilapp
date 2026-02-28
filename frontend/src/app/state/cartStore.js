import { create } from 'zustand'

const STORAGE_KEY = 'cart-items'

const readInitial = () => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch {
    return []
  }
}

export const useCartStore = create((set, get) => ({
  items: readInitial(),
  add: (product) => {
    const exists = get().items.find((it) => it.product_id === product.id)
    const items = exists
      ? get().items.map((it) =>
          it.product_id === product.id ? { ...it, qty: it.qty + 1 } : it,
        )
      : [...get().items, { product_id: product.id, name: product.name, price: Number(product.price), qty: 1 }]

    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
    set({ items })
  },
  remove: (productId) => {
    const items = get().items.filter((it) => it.product_id !== productId)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
    set({ items })
  },
  clear: () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([]))
    set({ items: [] })
  },
  subtotal: () => get().items.reduce((acc, it) => acc + it.price * it.qty, 0),
}))
