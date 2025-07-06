import { API_URL } from './env'

export const login = async () => {
  const res = await fetch(`${API_URL}/login`)
  let url = await res.text()
  return url.trim().replace(/^"|"$/g, '')
}

export const getUserInfo = async () => {
  const res = await fetch(`${API_URL}/users/me`, { credentials: 'include' })
  const user = await res.json()
  return { name: user.full_name, avatar: user.avatar }
}
