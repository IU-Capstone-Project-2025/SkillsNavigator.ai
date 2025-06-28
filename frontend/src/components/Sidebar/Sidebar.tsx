import { Tooltip } from '@mantine/core'
import { useState } from 'react'
import arrowsLeft from '/assets/arrowsLeft.png'
import arrowsRight from '/assets/arrowsRight.png'
import squarePen from '/assets/squarePen.png'
import roadmapIcon from '/assets/roadmapIcon.png'
import css from './index.module.scss'

type ChatItem = {
  id: number
  title: string
  active?: boolean
}

type SidebarProps = {
  chats: ChatItem[]
  onSelect: (id: number) => void
}

export const Sidebar: React.FC<SidebarProps> = ({ chats, onSelect }) => {
  const [open, setOpen] = useState(true)

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
          <button className={css.newChat}>
            <img src={squarePen} width={18} />
            Новый чат
          </button>
        </div>
        <ul className={css.chatList}>
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`${css.chatItem} ${chat.active ? css.active : ''}`}
              onClick={() => onSelect(chat.id)}
            >
              {chat.title}
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
