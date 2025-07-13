import loadingGif from '/assets/loading.gif'
import css from './index.module.scss'

type MessageProps = {
  text: string
  isUser: boolean
  animate?: boolean
  loading?: boolean
}

const Message: React.FC<MessageProps> = ({ text, isUser, animate, loading=false }) => {
  const error = text === 'Упс, что-то пошло не так... Повторите попытку позже'

  return (
    <div className={`${css.wrapper} ${isUser ? css.userWrapper : css.friendWrapper}`}>
      <div
        className={`${css.bubble} ${isUser ? css.userBubble : css.friendBubble} ${animate ? css.animate : ''} ${error ? css.errorBubble : ''}`}
        data-testid={error ? 'errorBubble' : undefined}
      >
        {!loading ? text : <img src={loadingGif} width={30}/>}
        <div className={`${isUser ? css.userTail : css.friendTail} ${error ? css.errorTail : ''}`} />
      </div>
    </div>
  )
}

export default Message
