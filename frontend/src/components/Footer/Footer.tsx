import { NavLink } from '..'
import * as routes from '../../lib/routes'
import css from './index.module.scss'

const Footer = () => {
  return (
    <div>
      <footer className={css.footer}>
        <div className={css.nav}>
          <h4 className={css.headline}>Навигация</h4>
          <div className={css.links}>
            <NavLink text="Главная" to={routes.getMainRoute()} />
            <NavLink text="Чат" to={routes.getChatRoute()} />
            <NavLink text="Мой путь" to={routes.getRoadmapRoute()} disabled />
            <NavLink text="О нас" to={routes.getAboutRoute()} disabled />
          </div>
        </div>
        <div className={css.contacts}>
          <h4 className={css.headline}>Свяжитесь с нами</h4>
          <div className={css.contactsList}>
            <div>mail@gmail.com</div>
            <div>@alias</div>
          </div>
        </div>
      </footer>
      <div className={css.bottomSection}>SkillsNavigator 2025</div>
    </div>
  )
}
export default Footer
