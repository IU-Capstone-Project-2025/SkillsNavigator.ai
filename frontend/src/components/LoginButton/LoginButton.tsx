import stepikIcon from '/assets/stepikIcon.png'
import { useAuth } from '../../lib/AuthProvider'
import css from './index.module.scss'

const LoginButton: React.FC<{ text: string }> = ({ text }) => {
  const { handleLogin } = useAuth()

  return (
    <button className={css.button} onClick={handleLogin}>
      <span>{text}</span>
      <img src={stepikIcon} width={18} />
    </button>
  )
}

export default LoginButton
