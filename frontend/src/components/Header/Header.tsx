import logo from '/assets/logo.png'
import { useState } from 'react'
import { LoginModal, NavLink } from '../'
import * as routes from '../../lib/routes'
import css from './index.module.scss'

const Header = () => {
  const [openedLogin, setOpenedLogin] = useState(false)

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

      <button className={css.loginButton} onClick={() => setOpenedLogin(true)}>
        Вход
      </button>

      <LoginModal opened={openedLogin} onClose={() => setOpenedLogin(false)} />
    </div>
  )
}
export default Header
