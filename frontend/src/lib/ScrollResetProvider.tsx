import React, { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

const ScrollResetProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [location])

  return <>{children}</>
}

export default ScrollResetProvider
