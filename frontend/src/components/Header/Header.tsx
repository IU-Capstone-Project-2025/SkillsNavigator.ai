import logo from '/assets/logo.png'
import css from './index.module.scss'
import { NavLink } from '../'
import * as routes from '../../lib/routes'

const Header = () => {
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
        <NavLink text="Мой путь" to={routes.getRoadmapRoute()} disabled />
        <NavLink text="О нас" to={routes.getAboutRoute()} disabled />
      </div>

      <button className={css.loginButton}>Вход</button>
    </div>
  )
}
export default Header
