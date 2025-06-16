import { NavLink } from 'react-router-dom'
import css from './index.module.scss'

type NavigationLinkProps = {
  text: string
  to: string
  disabled?: boolean
}

const NavigationLink: React.FC<NavigationLinkProps> = ({ text, to, disabled = false }) =>
  !disabled ? (
    <NavLink className={({ isActive }) => (isActive ? css.activeLink : css.link)} to={to}>
      {text}
    </NavLink>
  ) : (
    <h5 className={css.disabled}>{text}</h5>
  )

export default NavigationLink
