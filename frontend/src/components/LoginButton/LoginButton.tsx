import stepikIcon from '/assets/stepikIcon.png'
import css from './index.module.scss'

const LoginButton: React.FC<{ text: string }> = ({ text }) => {
  return (
    <button className={css.button} onClick={() => {}}>
      <span>{text}</span>
      <img src={stepikIcon} width={18} />
    </button>
  )
}

export default LoginButton
