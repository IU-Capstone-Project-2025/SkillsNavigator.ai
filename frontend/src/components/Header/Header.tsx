import logo from '/assets/logo.png'
import chevronDown from '/assets/chevronDown.png'
import { useState } from 'react'
import { LoginModal, NavLink } from '../'
import { useAuth } from '../../lib/AuthProvider'
import * as routes from '../../lib/routes'
import css from './index.module.scss'

const Header = () => {
  const [openedLogin, setOpenedLogin] = useState(false)
  const [userHovered, setUserHovered] = useState(false)
  const { authenticated, name, avatar } = useAuth()

  return (
    <div className={css.header}>
      <a href={routes.getMainRoute()}>
        <div className={css.logoContainer}>
          <img src={logo} alt="" className={css.logo} />
          <h4 className={css.title}>SkillsNavigator</h4>
        </div>
      </a>

      <div className={css.links}>
        <NavLink text="Главная" to={routes.getMainRoute()} />
        <NavLink text="Чат" to={routes.getChatRoute()} />
        <NavLink text="Мой путь" to={routes.getRoadmapRoute()} />
      </div>

      {!authenticated ? (
        <button className={css.loginButton} onClick={() => setOpenedLogin(true)}>
          Вход
        </button>
      ) : (
        <div
          className={css.userWrapper}
          onMouseEnter={() => setUserHovered(true)}
          onMouseLeave={() => setUserHovered(false)}
        >
          <div className={css.user}>
            <img src={avatar} width={20} />
            <span>{name}</span>
            <img src={chevronDown} width={20} className={css.chevronIcon} />
          </div>
          {userHovered && (
            <button className={css.logoutButton}>
              Выйти
            </button>
          )}
        </div>
      )}

      <LoginModal opened={openedLogin} onClose={() => setOpenedLogin(false)} />
    </div>
  )
}
export default Header
