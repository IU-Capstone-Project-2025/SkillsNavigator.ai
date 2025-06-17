import { useRef, useState, useEffect } from 'react'
import { CardInChat, Input, Message } from '../../components'
import { courses, questions } from '../../lib/data'
import css from './index.module.scss'

type Answers = {
  area: string
  current_level: string
  desired_skills: string
}

type ChatMessage = {
  text: string
  isUser: boolean
}

const PLACEHOLDER_COUNT = 3

const answerKeys: (keyof Answers)[] = ['area', 'current_level', 'desired_skills']

const Chat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([{ text: questions[0].text, isUser: false }])
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Partial<Answers>>({})
  const [inputValue, setInputValue] = useState('')
  const [shownCourses, setShownCourses] = useState<number>(0)
  const chatEndRef = useRef<HTMLDivElement>(null)

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
      }, 800)
    }

    scrollToBottom()
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend()
    }
  }

  // Показываем курсы по одному с задержкой после завершения вопросов
  useEffect(() => {
    if (step === questions.length - 1 && answers.desired_skills) {
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
  }, [step, answers.desired_skills])

  // Прокрутка вниз при каждом рендере
  useEffect(() => {
    scrollToBottom()
    // eslint-disable-next-line
  }, [messages, shownCourses])

  return (
    <div className={css.root}>
      <div className={css.chat}>
        {messages.map((msg, idx) => (
          <Message key={idx} text={msg.text} isUser={msg.isUser} animate={idx === messages.length - 1} />
        ))}

        <div className={css.courses}>
  {step === questions.length - 1 && answers.desired_skills && (
    <>
      {courses.slice(0, shownCourses).map((course) => (
        <CardInChat {...course} key={course.id} />
      ))}
      {/* Добавляем невидимые плейсхолдеры, если курсов меньше 3 */}
      {Array.from({ length: Math.max(0, PLACEHOLDER_COUNT - shownCourses) }).map((_, idx) => (
        <div className={css.placeholderCard} key={`placeholder-${idx}`} />
      ))}
    </>
  )}
</div>
        <div ref={chatEndRef} />
      </div>
      {step < questions.length && (
        <Input
          width="100%"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onSend={handleSend}
          placeholder="Введите ответ..."
        />
      )}
    </div>
  )
}

export default Chat
