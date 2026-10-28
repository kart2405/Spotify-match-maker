// In development Vite proxies /api to the backend. In production set VITE_API_URL.
const API_URL = import.meta.env.VITE_API_URL ?? ''

export async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${API_URL}/api${path}`, {
    method,
    credentials: 'include',
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const error = new Error(data?.detail ?? `Request failed (${res.status})`)
    error.status = res.status
    throw error
  }
  return data
}

export const spotifyLoginUrl = `${API_URL}/api/auth/spotify/login`
