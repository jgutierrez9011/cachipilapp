import { Navigate, Route, Routes } from 'react-router-dom'

import Checkout from './pages/Checkout'
import OrderCreated from './pages/OrderCreated'
import StoreFront from './pages/StoreFront'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/t/:slug" element={<StoreFront />} />
      <Route path="/t/:slug/checkout" element={<Checkout />} />
      <Route path="/t/:slug/order-created" element={<OrderCreated />} />
      <Route path="*" element={<Navigate to="/t/demo" replace />} />
    </Routes>
  )
}
