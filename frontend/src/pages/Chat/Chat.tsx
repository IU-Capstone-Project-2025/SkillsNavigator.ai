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
  const [messages, setMessages] = useState<MessageType[]>([{ text: questions[0].text, isUser: false }])
  const [loadingChats, setLoadingChats] = useState(false)
  const [coursesLoading, setCoursesLoading] = useState(false)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  // /api/getChats
  useEffect(() => {
    const fetchChats = async () => {
      setLoadingChats(true)
      const chats: ChatType[] = await getChats()
      // Помечаем сообщения с нечетным индексом как isUser: true
      const normalizedChats = chats.map((chat) => ({
        ...chat,
        messages: chat.messages.map((msg, idx) => ({
          ...msg,
          isUser: idx % 2 === 1, // нечетный индекс — пользователь
        })),
      }))
      setLocalChats(normalizedChats)
      setLoadingChats(false)
    }

    if (authenticated) {
      fetchChats()
    }
  }, [])

  const handleSend = async () => {
    if (!inputValue.trim()) {
      return
    }

    let chatId = activeChat
    let newMessages = [...messages]
    let msgNumber = messages.length + 1 // Счётчик сообщений (начинается с 1)

    // Если это первый ответ — создаём чат и сохраняем первый вопрос и ответ
    if (step === 0 && activeChat === -1) {
      chatId = await createChat()
      setActiveChat(chatId)

      // Сохраняем первый вопрос (messageNumber = 1)
      await saveMessage(chatId, questions[0].text, 1)
      // Сохраняем первый ответ (messageNumber = 2)
      await saveMessage(chatId, inputValue, 2)

      newMessages = [
        { text: questions[0].text, isUser: false },
        { text: inputValue, isUser: true },
      ]
      setMessages(newMessages)
      setLocalChats((prev) => [...prev, { id: chatId, name: inputValue, roadmapId: 0, messages: newMessages }])
    } else {
      // Сохраняем ответ пользователя (messageNumber = messages.length + 1)
      if (chatId !== -1) {
        await saveMessage(chatId, inputValue, msgNumber)
      }
      newMessages = [...messages, { text: inputValue, isUser: true }]
      setMessages(newMessages)
      setLocalChats((prevChats) =>
        prevChats.map((chat) =>
          chat.id === chatId ? { ...chat, messages: [...chat.messages, { text: inputValue, isUser: true }] } : chat
        )
      )
    }

    setInputValue('')

    // Добавляем следующий вопрос, если он есть
    if (step + 1 < questions.length) {
      setTimeout(async () => {
        const botMsg = { text: questions[step + 1].text, isUser: false }
        const updatedMessages = [...newMessages, botMsg]
        setMessages(updatedMessages)

        if (chatId !== -1) {
          await saveMessage(chatId, questions[step + 1].text, updatedMessages.length)
          setLocalChats((prevChats) =>
            prevChats.map((chat) => (chat.id === chatId ? { ...chat, messages: [...chat.messages, botMsg] } : chat))
          )
        }

        setStep((prev) => prev + 1)
        scrollToBottom()
      }, 400)
    } else {
      handleSearch({
        area: messages[1]?.text,
        current_level: messages[3]?.text,
        desired_skills: inputValue,
      })
      if (coursesInsertIndex === null) {
        setCoursesInsertIndex(messages.length)
      }
    }
    scrollToBottom()
  }

  // BUILD ROADMAP
  const handleSearch = async (payload: PayloadType) => {
    setCoursesLoading(true)
    try {
      const data = await searchCourses(payload, activeChat)
      const answerMessage = {
        text: 'Твой план, который приведет к цели:',
        isUser: false,
      }
      setMessages((prev) => {
        const updated = [...prev, answerMessage]
        setCoursesInsertIndex(updated.length + 1)
        if (activeChat !== -1) {
          setLocalChats((prevChats) =>
            prevChats.map((chat) => (chat.id === activeChat ? { ...chat, chat: updated } : chat))
          )
        }

        return updated
      })
      setCourses(data)
    } catch {
      const errorMessage = {
        text: 'Упс, что-то пошло не так... Повторите попытку позже',
        isUser: false,
      }
      await saveMessage(activeChat, errorMessage.text, messages.length + 1)

      setMessages((prev) => {
        const updated = [...prev, errorMessage]

        if (activeChat !== -1) {
          setLocalChats((prevChats) =>
            prevChats.map((chat) => (chat.id === activeChat ? { ...chat, chat: updated } : chat))
          )
        }

        return updated
      })
    } finally {
      setCoursesLoading(false)
    }
  }

  // NEW CHAT FROM MAIN
  useEffect(() => {
    const saved = localStorage.getItem('chatInput')
    if (saved) {
      const newId = Math.max(...localChats.map((c) => c.id), 0) + 1
      const newMessages = [
        { text: questions[0].text, isUser: false },
        { text: saved, isUser: true },
        { text: questions[1].text, isUser: false },
      ]
      const newChat: ChatType = {
        id: newId,
        name: saved,
        roadmapId: 0,
        messages: newMessages,
      }
      setLocalChats([newChat, ...localChats])
      setActiveChat(newId)
      setMessages(newMessages)
      setStep(1)
      setInputValue('')
      localStorage.removeItem('chatInput')
    }
  }, [])

  const scrollToBottom = () => {
    setTimeout(() => {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  // onSelect — полностью восстанавливает состояние по истории чата
  const onSelect = (id: number) => {
    setActiveChat(id)
    const chat = localChats.find((c) => c.id === id)
    const chatMessages = chat?.messages ?? []
    setMessages(chatMessages)
    setStep(chatMessages.filter((m) => !m.isUser).length - 1)
    setInputValue('')
    setCourses([])
    setCoursesInsertIndex(null)
  }

  // ANIMATIONS
  useEffect(() => {
    if (courses.length > 0) {
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
  }, [messages])

  useEffect(() => {
    if (shownCourses === courses.length && courses.length > 0) {
      scrollToBottom()
    }
  }, [shownCourses, courses.length])

  const messagesBeforeCourses = coursesInsertIndex !== null ? messages.slice(0, coursesInsertIndex) : messages
  const messagesAfterCourses = coursesInsertIndex !== null ? messages.slice(coursesInsertIndex) : []

  const handleNewChat = () => {
    setActiveChat(-1)
    setMessages([{ text: questions[0].text, isUser: false }])
    setCourses([])
    setCoursesInsertIndex(null)
    setShownCourses(0)
    setStep(0)
  }

  if (loadingChats && authenticated) {
    return (
      <div className={css.root}>
        <Loading />
      </div>
    )
  }

  return (
    <div className={css.root}>
      <Sidebar chats={localChats} activeChat={activeChat} onSelect={(id) => onSelect(id)} onNewChat={handleNewChat} />

      <div className={css.chat} ref={chatContainerRef}>
        <>
          {messagesBeforeCourses.map((msg, idx) => {
            const isLast = idx === messagesBeforeCourses.length - 1
            return <Message key={idx} text={msg.text} isUser={msg.isUser} animate={isLast} />
          })}

          {courses.length > 0 ? (
            <div className={css.courses}>
              {step === questions.length - 1 && messages.length === 6 && (
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
            coursesLoading && (
              <div className={css.courses}>
                <Message text="" loading isUser={false} />
              </div>
            )
          )}

          {messagesAfterCourses.map((msg, idx) => (
            <Message key={`after-${idx}`} text={msg.text} isUser={msg.isUser} animate={false} />
          ))}
        </>

        {shownCourses === courses.length && courses.length > 0 && (
          <button
            className={css.goToRoadmapButton}
            onClick={() => {
              navigate(getRoadmapRoute())
            }}
          >
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
}

export default Chat
