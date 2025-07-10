import { useRef, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { createChat, getChats, saveMessage, searchCourses } from '../../api/api'
import { Card, Input, Loading, Message, Sidebar } from '../../components'
import { useAuth } from '../../lib/AuthProvider'
import { questions } from '../../lib/data'
import { getRoadmapRoute } from '../../lib/routes'
import { ChatType, CourseType, MessageType, PayloadType } from '../../lib/types'
import css from './index.module.scss'

const PLACEHOLDER_COUNT = 3

const Chat = () => {
  const navigate = useNavigate()
  const authenticated = useAuth().authenticated
  const [step, setStep] = useState(0)
  const [inputValue, setInputValue] = useState('')
  const [shownCourses, setShownCourses] = useState<number>(0)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const [courses, setCourses] = useState<CourseType[]>([])
  const [coursesInsertIndex, setCoursesInsertIndex] = useState<number | null>(null)
  const [activeChat, setActiveChat] = useState<number>(-1)
  const [localChats, setLocalChats] = useState<ChatType[]>([])
  const [loadingChats, setLoadingChats] = useState(false)
  const [coursesLoading, setCoursesLoading] = useState(false)
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const currentChat = localChats.find((c) => c.id === activeChat)
  const chatMessages = currentChat?.messages ?? [{ text: questions[0].text, isUser: false }]

  const answerKeys: (keyof PayloadType)[] = ['area', 'current_level', 'desired_skills']
  const [guestStep, setGuestStep] = useState(0)
  const [guestAnswers, setGuestAnswers] = useState<Partial<PayloadType>>({})
  const [guestMessages, setGuestMessages] = useState([{ text: questions[0].text, isUser: false }])
  const [guestCourses, setGuestCourses] = useState<CourseType[]>([])
  const [guestCoursesLoading, setGuestCoursesLoading] = useState(false)

  const guestSendAnswer = async () => {
    const key = answerKeys[guestStep]
    const newAnswers = { ...guestAnswers, [key]: inputValue }
    setGuestAnswers(newAnswers)
    setGuestMessages((prev) => [...prev, { text: inputValue, isUser: true }])

    if (guestStep < answerKeys.length - 1) {
      setGuestMessages((prev) => [...prev, { text: questions[guestStep + 1].text, isUser: false }])
      setGuestStep(guestStep + 1)
      setInputValue('')
    } else {
      setGuestCoursesLoading(true)
      try {
        const data = await searchCourses(newAnswers as PayloadType)
        setGuestCourses(data)
        setGuestMessages((prev) => [
          ...prev,
          { text: 'Твой план, который приведет к цели:', isUser: false },
          { text: 'roadmapCourses000: ' + JSON.stringify(data), isUser: false },
        ])
      } catch {
        setGuestMessages((prev) => [
          ...prev,
          { text: 'Упс, что-то пошло не так... Повторите попытку позже', isUser: false },
        ])
      } finally {
        setGuestCoursesLoading(false)
      }
    }
  }

  useEffect(() => {
    const fetchChats = async () => {
      setLoadingChats(true)
      const chats: ChatType[] = await getChats()
      const normalizedChats = chats.map((chat) => ({
        ...chat,
        messages: chat.messages.map((msg, idx) => ({
          ...msg,
          isUser: idx % 2 === 1,
        })),
      }))
      setLocalChats(normalizedChats)
      setLoadingChats(false)
    }

    if (authenticated) {
      fetchChats()
    }

    if (!authenticated) {
      const saved = localStorage.getItem('chatInput')
      if (saved) {
        setGuestMessages([
          { text: questions[0].text, isUser: false },
          { text: saved, isUser: true },
          { text: questions[1].text, isUser: false },
        ])
        setGuestAnswers({ [answerKeys[0]]: saved })
        setGuestStep(1)
        setInputValue('')
        localStorage.removeItem('chatInput')
      }
    } else {
      const saved = localStorage.getItem('chatInput')
      if (saved) {
        setInputValue(saved)
        setPendingInputFromStorage(true)
        localStorage.removeItem('chatInput')
      }
    }
  }, [authenticated])

  const addMessageToChat = async (chatId: number, message: MessageType) => {
    setLocalChats((prevChats) =>
      prevChats.map((chat) => (chat.id === chatId ? { ...chat, messages: [...chat.messages, message] } : chat))
    )
    await saveMessage(chatId, message.text, (localChats.find((c) => c.id === chatId)?.messages.length ?? 0) + 1)
    setInputValue('')
    scrollToBottom()
  }

  const handleSend = async () => {
    if (!inputValue.trim()) {
      return
    }

    let chatId = activeChat

    if (step === 0 && activeChat === -1) {
      chatId = await createChat()
      setActiveChat(chatId)
      const message1 = { text: questions[0].text, isUser: false }
      await addMessageToChat(chatId, message1)
      setLocalChats((prev) => [...prev, { id: chatId, name: inputValue, roadmap_id: 0, messages: [message1] }])
    }

    await addMessageToChat(chatId, { text: inputValue, isUser: true })

    if (step + 1 < questions.length) {
      setTimeout(async () => {
        await addMessageToChat(chatId, { text: questions[step + 1].text, isUser: false })
        setStep((prev) => prev + 1)
      }, 400)
    } else {
      handleSearch({
        area: chatMessages[1]?.text,
        current_level: chatMessages[3]?.text,
        desired_skills: inputValue,
      })
      if (coursesInsertIndex === null) {
        setCoursesInsertIndex(chatMessages.length)
      }
    }
  }

  const handleSearch = async (payload: PayloadType) => {
    setCoursesLoading(true)
    try {
      const data = await searchCourses(payload, activeChat)
      await addMessageToChat(activeChat, { text: 'Твой план, который приведет к цели:', isUser: false })
      await addMessageToChat(activeChat, { text: 'roadmapCourses000: ' + JSON.stringify(data), isUser: false })
      setCourses(data)
    } catch {
      await addMessageToChat(activeChat, { text: 'Упс, что-то пошло не так... Повторите попытку позже', isUser: false })
    } finally {
      setCoursesLoading(false)
    }
  }

  const [pendingInputFromStorage, setPendingInputFromStorage] = useState(false)

  useEffect(() => {
    if (pendingInputFromStorage && inputValue) {
      handleSend()
      setPendingInputFromStorage(false)
    }
  }, [localChats])

  const scrollToBottom = () => {
    setTimeout(() => {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  const onSelect = (id: number) => {
    setActiveChat(id)
    const chat = localChats.find((c) => c.id === id)
    const chatMessages = chat?.messages ?? []
    setStep(chatMessages.filter((m) => !m.isUser).length - 1)
    setInputValue('')
    setCourses([])
    setCoursesInsertIndex(null)

    const coursesMsg = chatMessages.find((msg) => msg.text.startsWith('roadmapCourses000:'))
    if (coursesMsg) {
      const coursesArr: CourseType[] = JSON.parse(coursesMsg.text.replace('roadmapCourses000: ', ''))
      setCourses(coursesArr)
      setShownCourses(coursesArr.length)
    }
  }

  useEffect(() => {
    if (courses.length > 0 && shownCourses < courses.length) {
      setShownCourses(0)
      let i = 0
      const interval = setInterval(() => {
        i++
        setShownCourses(i)
        if (i >= courses.length) {
          clearInterval(interval)
        }
      }, 500)
      return () => clearInterval(interval)
    }
  }, [courses])

  useEffect(() => {
    scrollToBottom()
  }, [shownCourses])

  const handleNewChat = () => {
    setActiveChat(-1)
    setCourses([])
    setCoursesInsertIndex(null)
    setShownCourses(0)
    setStep(0)
  }

  const lastMsgIdx = (() => {
    let idx = -1
    chatMessages.forEach((msg, i) => {
      if (!msg.text.startsWith('roadmapCourses000:')) {
        idx = i
      }
    })
    return idx
  })()

  const gotoRoadmap = () => {
    navigate(getRoadmapRoute())
    localStorage.setItem('roadmapId', localChats.find((c) => c.id === activeChat)?.roadmap_id.toString() || '-1')
  }

  if (loadingChats && authenticated) {
    return (
      <div className={css.root}>
        <Loading />
      </div>
    )
  }

  if (authenticated) {
    return (
      <div className={css.root}>
        <Sidebar chats={localChats} activeChat={activeChat} onSelect={(id) => onSelect(id)} onNewChat={handleNewChat} />

        <div className={css.chat} ref={chatContainerRef}>
          {chatMessages.map((msg, idx) => {
            if (msg.text.startsWith('roadmapCourses000:')) {
              let coursesArr: CourseType[] = []
              try {
                coursesArr = JSON.parse(msg.text.replace('roadmapCourses000: ', ''))
              } catch {}
              return (
                <div className={css.courses} key={`courses-${idx}`}>
                  {coursesArr.slice(0, shownCourses).map((course, i) => (
                    <Card {...course} key={course.id} index={i} inChat />
                  ))}
                  {coursesLoading && (
                    <div className={css.courses}>
                      <Message text="" loading isUser={false} />
                    </div>
                  )}
                  {Array.from({ length: Math.max(0, PLACEHOLDER_COUNT - shownCourses) }).map((_, i) => (
                    <div className={css.placeholderCard} key={`placeholder-${i}`} />
                  ))}
                </div>
              )
            }
            const isLast = idx === lastMsgIdx
            return <Message key={idx} text={msg.text} isUser={msg.isUser} animate={isLast} />
          })}

          {shownCourses === courses.length && courses.length > 0 && (
            <button className={css.goToRoadmapButton} onClick={gotoRoadmap}>
              Перейти к пути
            </button>
          )}

          <div ref={chatEndRef} />
        </div>

        <Input
          width="100%"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSend={handleSend}
          placeholder="Введите ответ..."
          focus
        />
      </div>
    )
  } else {
    return (
      <div className={css.root}>
        <Sidebar chats={localChats} activeChat={activeChat} onSelect={(id) => onSelect(id)} onNewChat={handleNewChat} />

        <div className={css.chat} ref={chatContainerRef}>
          <>
            {guestMessages.map((msg, idx) => {
              const isLast = idx === guestMessages.length - 1
              return <Message key={idx} text={msg.text} isUser={msg.isUser} animate={isLast} />
            })}

            {guestCourses.length > 0 ? (
              <div className={css.courses}>
                {step === questions.length - 1 && guestMessages.length === 6 && (
                  <>
                    {courses.slice(0, shownCourses).map((course, idx) => (
                      <Card {...course} key={course.id} index={idx} inChat />
                    ))}
                    {Array.from({ length: Math.max(0, PLACEHOLDER_COUNT - shownCourses) }).map((_, idx) => (
                      <div className={css.placeholderCard} key={`placeholder-${idx}`} />
                    ))}
                  </>
                )}
              </div>
            ) : (
              guestCoursesLoading && (
                <div className={css.courses}>
                  <Message text="" loading isUser={false} />
                </div>
              )
            )}
          </>
          <div ref={chatEndRef} />
        </div>

        <Input
          width="100%"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSend={guestSendAnswer}
          placeholder="Введите ответ..."
          focus
        />
      </div>
    )
  }
}

export default Chat
