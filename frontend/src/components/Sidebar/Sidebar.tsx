import { Tooltip } from '@mantine/core'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import arrowsLeft from '/assets/arrowsLeft.png'
import arrowsRight from '/assets/arrowsRight.png'
import squarePen from '/assets/squarePen.png'
import roadmapIcon from '/assets/roadmapIcon.png'
import lockIcon from '/assets/lock.png'
import mark from '/assets/mark.png'
import filledMark from '/assets/filledMark.png'
import doneImage from '/assets/doneImage.png'
import { useAuth } from '../../lib/AuthProvider'
import { getRoadmapRoute } from '../../lib/routes'
import { ChatType, RoadmapType } from '../../lib/types'
import LoginButton from '../LoginButton/LoginButton'
import css from './index.module.scss'

type SidebarProps = {
  chats: ChatType[]
  activeChat: number
  onSelect: (id: number) => void
  onNewChat: () => void
  isRoadmap?: boolean
  roadmaps?: RoadmapType[]
  onToggleStatus?: (id: number) => void
}

export const Sidebar: React.FC<SidebarProps> = ({
  chats,
  activeChat,
  onSelect,
  onNewChat,
  isRoadmap = false,
  roadmaps = [],
  onToggleStatus,
}) => {
  const navigate = useNavigate()
  const authenticated = useAuth().authenticated
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
            <h4>{!isRoadmap ? 'Чаты' : 'Мои путь'}</h4>
            <button className={css.collapseBtn} onClick={() => setOpen(false)}>
              <img src={arrowsLeft} width={24} />
            </button>
          </div>
          <button className={css.newChat} onClick={onNewChat}>
            <img src={squarePen} width={18} />
            {!isRoadmap ? 'Новый чат' : 'Новый путь'}
          </button>
        </div>
        <ul className={authenticated ? `${css.chatList}` : `${css.chatList} ${css.blockChatHistory}`}>
          {chats.length > 0 &&
            [...chats]
              .sort((a, b) => b.id - a.id)
              .map((chat, index) => (
                <div
                  key={chat.id}
                  className={`${css.chatItem} ${chat.id === activeChat ? css.active : ''}`}
                  onClick={() => onSelect(chat.id)}
                >
                  <h5 className={css.chatName}>
                    {chat.name}
                  </h5>
                  {!isRoadmap ? (
                    <Tooltip label="Перейти к пути" position="bottom-start" openDelay={800}>
                      <img
                        src={roadmapIcon}
                        width={28}
                        height={28}
                        className={css.icon}
                        onClick={() => navigate(getRoadmapRoute())}
                      />
                    </Tooltip>
                  ) : roadmaps[index].status !== 'done' ? (
                    <Tooltip label="Прохожу сейчас" position="bottom-start" openDelay={800}>
                      <img
                        src={roadmaps[index].status !== 'current' ? mark : filledMark}
                        width={28}
                        height={28}
                        className={css.icon}
                        style={{visibility: 'hidden'}}
                        onClick={(e) => {
                          e.stopPropagation()
                          onToggleStatus?.(chat.id)
                        }}
                      />
                    </Tooltip>
                  ) : (
                    <img src={doneImage} width={25} height={25} style={{ borderRadius: '99px', opacity: '0.8', visibility: 'hidden' }} />
                  )}
                </div>
              ))}
        </ul>
        {!authenticated && !isRoadmap && (
          <div className={css.lockOverlay}>
            <div className={css.lockText}>
              <img src={lockIcon} className={css.lockIcon} alt="lock" />
              Войдите, чтобы сохранять историю
            </div>
            <LoginButton text="Войти" />
          </div>
        )}
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
