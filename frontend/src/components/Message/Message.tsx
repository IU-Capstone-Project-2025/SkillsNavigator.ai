import css from './index.module.scss'

type MessageProps = {
  text: string
  isUser: boolean
  animate?: boolean
  error?: boolean
}

const Message: React.FC<MessageProps> = ({ text, isUser, animate, error = false }) => {
  return (
    <div className={`${css.wrapper} ${isUser ? css.userWrapper : css.friendWrapper}`}>
      <div
        className={`${css.bubble} ${isUser ? css.userBubble : css.friendBubble} ${animate ? css.animate : ''} ${error ? css.errorBubble : ''}`}
      >
        {text}
        <div className={`${isUser ? css.userTail : css.friendTail} ${error ? css.errorTail : ''}`} />
      </div>
    </div>
  )
}

export default Message
