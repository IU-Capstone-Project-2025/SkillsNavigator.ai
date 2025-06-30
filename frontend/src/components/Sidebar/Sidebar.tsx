import { Tooltip } from '@mantine/core'
import { useEffect, useState } from 'react'
import arrowsLeft from '/assets/arrowsLeft.png'
import arrowsRight from '/assets/arrowsRight.png'
import squarePen from '/assets/squarePen.png'
import roadmapIcon from '/assets/roadmapIcon.png'
import { ChatType } from '../../lib/types'
import css from './index.module.scss'

type SidebarProps = {
  chats: ChatType[]
  activeChat: number
  onSelect: (id: number) => void
  onNewChat: () => void
}

export const Sidebar: React.FC<SidebarProps> = ({ chats, activeChat, onSelect, onNewChat }) => {
  const [open, setOpen] = useState(() => {
    const saved = localStorage.getItem('sidebarOpen')
    return saved === null ? false : saved === 'true'
  })

  useEffect(() => {
    localStorage.setItem('sidebarOpen', String(open))
  }, [open])

  return (
    <>
      <aside className={`${css.sidebar} ${open ? css.open : css.closed}`}>
        <div className={css.upperSection}>
          <div className={css.title}>
            <h4>Чаты</h4>
            <button className={css.collapseBtn} onClick={() => setOpen(false)}>
              <img src={arrowsLeft} width={24} />
            </button>
          </div>
          <button className={css.newChat} onClick={onNewChat}>
            <img src={squarePen} width={18} />
            Новый чат
          </button>
        </div>
        <ul className={css.chatList}>
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`${css.chatItem} ${chat.id === activeChat ? css.active : ''}`}
              onClick={() => onSelect(chat.id)}
            >
              <h5 className={css.chatName}>{chat.name}</h5>
              <Tooltip label="Перейти к пути" position="bottom-start" openDelay={800}>
                <img src={roadmapIcon} width={28} className={css.icon} />
              </Tooltip>
            </div>
          ))}
        </ul>
      </aside>
      {!open && (
        <button className={css.expandBtn} onClick={() => setOpen(true)}>
          <img src={arrowsRight} width={22} />
        </button>
      )}
    </>
  )
}

export default Sidebar
