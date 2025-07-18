import { API_URL } from './env'

export const login = async () => {
  const res = await fetch(`${API_URL}/login`)
  let url = await res.text()
  return url.trim().replace(/^"|"$/g, '')
}

export const getUserInfo = async () => {
  const res = await fetch(`${API_URL}/users/me`, { credentials: 'include' })
  if (!res.ok) {
    throw new Error('Not authenticated')
  }
  const user = await res.json()
  return { name:[user.first_name, user.last_name].filter(Boolean).join(' '), avatar: user.avatar }
}

export const logout = async () => {
  return `${API_URL}/logout`
}
