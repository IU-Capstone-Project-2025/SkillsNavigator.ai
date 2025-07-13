import { Modal } from '@mantine/core'
import crossIcon from '/assets/cross.png'
import LoginButton from '../LoginButton/LoginButton'
import css from './index.module.scss'

type LoginModalProps = {
  opened: boolean
  onClose: () => void
  withClose?: boolean
}

const Login: React.FC<LoginModalProps> = ({ opened, onClose, withClose = true }) => {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      centered
      size="lg"
      zIndex={95}
      withCloseButton={false}
      overlayProps={{
        backgroundOpacity: 0.1,
        blur: 4,
      }}
      transitionProps={{ transition: 'fade', duration: 200, timingFunction: 'ease-out' }}
      radius="lg"
    >
      <div className={css.content}>
        <h4 className={css.title}>Вход</h4>
        <div className={css.divider}></div>
        {withClose && <img src={crossIcon} width={20} className={css.crossIcon} onClick={onClose} />}
        <LoginButton text="Войдите с помощью Stepik" />
      </div>
    </Modal>
  )
}

export default Login
