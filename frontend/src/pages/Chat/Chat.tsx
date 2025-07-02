import { useRef, useState, useEffect } from 'react'
import { searchCourses } from '../../api/api'
import { Card, Input, Loading, Message, Sidebar } from '../../components'
import { questions } from '../../lib/data'
import { chats } from '../../lib/data'
import { ChatType, CourseType, MessageType, PayloadType } from '../../lib/types'
import css from './index.module.scss'

const PLACEHOLDER_COUNT = 3

const answerKeys: (keyof PayloadType)[] = ['area', 'current_level', 'desired_skills']

const Chat = () => {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Partial<PayloadType>>({})
  const [inputValue, setInputValue] = useState('')
  const [shownCourses, setShownCourses] = useState<number>(0)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const [courses, setCourses] = useState<CourseType[]>([])
  const [coursesInsertIndex, setCoursesInsertIndex] = useState<number | null>(null)
  const [activeChat, setActiveChat] = useState<number>(-1)
  const [localChats, setLocalChats] = useState<ChatType[]>(chats)
  const [messages, setMessages] = useState<MessageType[]>([{ text: questions[0].text, isUser: false }])
  const [isDraft, setIsDraft] = useState(true)
  const [draftMessages, setDraftMessages] = useState<MessageType[]>([{ text: questions[0].text, isUser: false }])
  const [draftStep, setDraftStep] = useState(0)
  const [draftInput, setDraftInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingChats, setLoadingChats] = useState(true)

  useEffect(() => {
    setLoadingChats(true)
    setTimeout(() => {
      setLocalChats(chats)
      setLoadingChats(false)
    }, 300)
  }, [])

  const handleSearch = async (payload: PayloadType) => {
    setLoading(true)
    try {
      const data = await searchCourses(payload)
      setCourses(data)
      const answerMessage = {
        text: 'Твой план, который приведет к цели:',
        isUser: false,
      }
      setMessages((prev) => {
        const updated = [...prev, answerMessage]

        if (activeChat !== -1) {
          setLocalChats((prevChats) =>
            prevChats.map((chat) => (chat.id === activeChat ? { ...chat, chat: updated } : chat))
          )
        }

        return updated
      })
    } catch {
      const errorMessage = {
        text: 'Упс, что-то пошло не так... Повторите попытку позже',
        isUser: false,
      }

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
      setLoading(false)
    }
  }

  useEffect(() => {
    const saved = localStorage.getItem('chatInput')
    if (saved) {
      setMessages([
        { text: questions[0].text, isUser: false },
        { text: saved, isUser: true },
        { text: questions[1].text, isUser: false },
      ])
      setStep(1)
      setInputValue('')
      answers.area = saved
      localStorage.removeItem('chatInput')
    }
  }, [])

  const scrollToBottom = () => {
    setTimeout(() => {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  const handleSend = () => {
    if (!inputValue.trim()) {
      return
    }

    const userMsg = { text: inputValue, isUser: true }
    const newMessages = [...messages, userMsg]

    const key = answerKeys[step]
    if (key) {
      setAnswers((prev) => ({ ...prev, [key]: inputValue }))
    }

    setMessages(newMessages)

    if (activeChat !== -1) {
      setLocalChats((prevChats) =>
        prevChats.map((chat) =>
          chat.id === activeChat
            ? {
                ...chat,
                chat: [...newMessages],
              }
            : chat
        )
      )
    }

    setInputValue('')

    if (step + 1 < questions.length) {
      setTimeout(() => {
        const botMsg = { text: questions[step + 1].text, isUser: false }
        const updatedMessages = [...newMessages, botMsg]

        setMessages(updatedMessages)

        if (activeChat !== -1) {
          setLocalChats((prevChats) =>
            prevChats.map((chat) =>
              chat.id === activeChat
                ? {
                    ...chat,
                    chat: [...updatedMessages],
                  }
                : chat
            )
          )
        }

        setStep((prev) => prev + 1)
        scrollToBottom()
      }, 400)
    }
    scrollToBottom()
  }

  useEffect(() => {
    if (step === questions.length - 1 && answers.desired_skills) {
      handleSearch({
        area: answers.area || '',
        current_level: answers.current_level || '',
        desired_skills: answers.desired_skills || '',
      })
      if (coursesInsertIndex === null) {
        setCoursesInsertIndex(messages.length)
      }
    }
  }, [step, answers.desired_skills])

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
  }, [messages, shownCourses])

  const messagesBeforeCourses = coursesInsertIndex !== null ? messages.slice(0, coursesInsertIndex) : messages
  const messagesAfterCourses = coursesInsertIndex !== null ? messages.slice(coursesInsertIndex) : []

  const handleNewChat = () => {
    setIsDraft(true)
    setDraftMessages([{ text: questions[0].text, isUser: false }])
    setDraftStep(0)
    setDraftInput('')
    setActiveChat(-1)
  }

  const handleDraftSend = () => {
    if (!draftInput.trim()) {
      return
    }

    const userMsg = { text: draftInput, isUser: true }
    const newMessages = [...draftMessages, userMsg]

    if (draftStep === 0) {
      setAnswers((prev) => ({ ...prev, area: draftInput }))

      const newId = Math.max(...localChats.map((c) => c.id), 0) + 1
      const newChat: ChatType = {
        id: newId,
        name: draftInput,
        roadmapId: 0,
        messages: [...newMessages, { text: questions[1].text, isUser: false }],
      }
      setLocalChats([newChat, ...localChats])
      setActiveChat(newId)
      setMessages(newChat.messages)
      setStep(1)
      setInputValue('')
      setIsDraft(false)
      setDraftMessages([])
      setDraftInput('')
    } else {
      const key = answerKeys[draftStep]
      setAnswers((prev) => ({ ...prev, [key]: draftInput }))

      setDraftStep(draftStep + 1)
      setDraftMessages([...newMessages, { text: questions[draftStep + 1].text, isUser: false }])
    }
  }

  const onSelect = (id: number) => {
    setActiveChat(id)
    const chat = localChats.find((c) => c.id === id)
    const messages = chat?.messages ?? []
    setMessages(messages)
    setStep(messages.filter((m) => !m.isUser).length - 1)
    setInputValue('')
    setCourses([])
    setCoursesInsertIndex(null)
    setIsDraft(false)

    const userAnswers: Partial<PayloadType> = {}
    let answerIdx = 0
    messages.forEach((msg) => {
      if (msg.isUser && answerIdx < answerKeys.length) {
        const key = answerKeys[answerIdx]
        userAnswers[key] = msg.text
        answerIdx++
      }
    })
    setAnswers(userAnswers)
  }

  if (loadingChats) {
    return (
      <div className={css.root}>
        <Loading />
      </div>
    )
  }

  return (
    <div className={css.root}>
      <Sidebar chats={localChats} activeChat={activeChat} onSelect={(id) => onSelect(id)} onNewChat={handleNewChat} />

      <div className={css.chat}>
        {loading ? (
          <Loading />
        ) : isDraft ? (
          draftMessages.map((msg, idx) => <Message key={idx} text={msg.text} isUser={msg.isUser} animate={false} />)
        ) : (
          <>
            {messagesBeforeCourses.map((msg, idx) => {
              const isLast = idx === messagesBeforeCourses.length - 1
              return <Message key={idx} text={msg.text} isUser={msg.isUser} animate={isLast} />
            })}

            {courses.length > 0 && (
              <div className={css.courses}>
                {step === questions.length - 1 && answers.desired_skills && (
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
            )}

            {messagesAfterCourses.map((msg, idx) => (
              <Message key={`after-${idx}`} text={msg.text} isUser={msg.isUser} animate={false} />
            ))}
          </>
        )}

        <div ref={chatEndRef} />
      </div>

      {isDraft && (
        <Input
          width="100%"
          value={draftInput}
          onChange={(e) => setDraftInput(e.target.value)}
          onSend={handleDraftSend}
          placeholder="Введите ответ..."
        />
      )}

      {!isDraft && (
        <Input
          width="100%"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSend={handleSend}
          placeholder="Введите ответ..."
          focus
        />
      )}
    </div>
  )
}

export default Chat
