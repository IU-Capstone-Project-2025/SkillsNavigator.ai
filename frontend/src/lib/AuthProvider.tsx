import { createContext, useContext, useEffect, useState } from 'react'
import { getUserInfo, login } from '../api/login'

type AuthContextType = {
  authenticated: boolean
  name: string
  avatar: string
  checkAuth: () => Promise<void>
  handleLogin: () => Promise<void>
}

const AuthContext = createContext<AuthContextType>({
  authenticated: false,
  name: '',
  avatar: '',
  checkAuth: async () => {},
  handleLogin: async () => {},
})

export const useAuth = () => useContext(AuthContext)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false)
  const [name, setName] = useState('')
  const [avatar, setAvatar] = useState('')

  const checkAuth = async () => {
    try {
      const res = await getUserInfo()
      setName(res.name)
      setAvatar(res.avatar)
      setAuthenticated(true)
    } catch {
      setAuthenticated(false)
      setName('')
      setAvatar('')
    }
  }

  const handleLogin = async () => {
    window.location.href = await login()
  }

  useEffect(() => {
    checkAuth()
  }, [])

  return (
    <AuthContext.Provider value={{ authenticated, name, avatar, checkAuth, handleLogin }}>
      {children}
    </AuthContext.Provider>
  )
}