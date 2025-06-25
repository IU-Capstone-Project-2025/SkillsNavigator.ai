import { useRef, useState, useEffect } from 'react'
import { searchCourses } from '../../api/api'
import { Card, Input, Message } from '../../components'
import { questions } from '../../lib/data'
import { CourseType, MessageType, PayloadType } from '../../lib/types'
import css from './index.module.scss'

const PLACEHOLDER_COUNT = 3

const answerKeys: (keyof PayloadType)[] = ['area', 'current_level', 'desired_skills']

const Chat = () => {
  const [messages, setMessages] = useState<MessageType[]>([{ text: questions[0].text, isUser: false }])
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Partial<PayloadType>>({})
  const [inputValue, setInputValue] = useState('')
  const [shownCourses, setShownCourses] = useState<number>(0)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const [courses, setCourses] = useState<CourseType[]>([])
  const [error, setError] = useState(false)
  const [coursesInsertIndex, setCoursesInsertIndex] = useState<number | null>(null)

  const handleSearch = async (payload: PayloadType) => {
    try {
      const data = await searchCourses(payload)
      setCourses(data)
    } catch {
      setError(true)
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
    setMessages((prev) => [...prev, userMsg])

    const key = answerKeys[step]
    setAnswers((prev) => ({ ...prev, [key]: inputValue }))

    setInputValue('')

    if (step + 1 < questions.length) {
      setTimeout(() => {
        setMessages((prev) => [...prev, { text: questions[step + 1].text, isUser: false }])
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

  return (
    <div className={css.root}>
      <div className={css.chat}>
        {messagesBeforeCourses.map((msg, idx) => {
          const isLast = idx === messagesBeforeCourses.length - 1
          if (error && isLast) {
            return (
              <Message
                key={idx}
                text="Упс, что-то пошло не так... Повторите попытку позже"
                isUser={false}
                error
                animate={isLast}
              />
            )
          }
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

        <div ref={chatEndRef} />
      </div>
      {step < questions.length && (
        <Input
          width="100%"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSend={handleSend}
          placeholder="Введите ответ..."
        />
      )}
    </div>
  )
}

export default Chat
