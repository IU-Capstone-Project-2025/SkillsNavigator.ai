import arrowDown from '/assets/arrowDown.png'
import { Transition } from '@mantine/core'
import css from './index.module.scss'

type Props = {
  show: boolean
  scrollToBottom: () => void
}

const ButtonScrollToBottom: React.FC<Props> = ({ show, scrollToBottom }) => {
  return (
    <Transition transition="slide-up" mounted={show}>
      {(transitionStyles) => (
        <button className={css.button} style={transitionStyles} onClick={scrollToBottom}>
          <img src={arrowDown} width={25} />
        </button>
      )}
    </Transition>
  )
}

export default ButtonScrollToBottom