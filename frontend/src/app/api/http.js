const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || 'Error de servidor')
  }

  return res.json()
}
