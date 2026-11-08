import { request, tokenStore } from './client'

export type User = { id: number; email: string }

export function register(email: string, password: string) {
  return request<User>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export async function login(email: string, password: string) {
  // the login endpoint expects a form, with the email in a field named "username"
  const body = new URLSearchParams({ username: email, password })
  const data = await request<{ access_token: string }>('/auth/login', {
    method: 'POST',
    body,
  })
  tokenStore.set(data.access_token)
}

export function getMe() {
  return request<User>('/auth/me')
}