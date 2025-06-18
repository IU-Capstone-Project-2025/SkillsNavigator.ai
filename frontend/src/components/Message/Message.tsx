import React from 'react'
import css from './index.module.scss'

type MessageProps = {
  text: string
  isUser: boolean
  animate?: boolean
}

const Message: React.FC<MessageProps> = ({ text, isUser, animate }) => {
  return (
    <div className={`${css.wrapper} ${isUser ? css.userWrapper : css.friendWrapper}`}>
    <div className={`${css.bubble} ${isUser ? css.userBubble : css.friendBubble} ${animate ? css.animate : ''}`}>
        {text}
        <div className={isUser ? css.userTail : css.friendTail} />
      </div>
    </div>
  )
}

export default Message
