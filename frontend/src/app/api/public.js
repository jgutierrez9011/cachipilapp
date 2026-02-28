import { request } from './http'

export const getStore = (slug) => request(`/public/stores/${slug}`)
export const getProducts = (slug) => request(`/public/stores/${slug}/products`)
export const createOrder = (payload) =>
  request('/public/orders', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
