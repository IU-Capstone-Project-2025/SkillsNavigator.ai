import roadmapMockup from '/assets/roadmap_mockup.png'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPopularCourses } from '../../api/api'
import { Card, Input, MoreButton } from '../../components'
import thoughts from '/assets/thoughts.png'
import arrowRight from '/assets/arrowRight.png'
import { getChatRoute } from '../../lib/routes'
import { CourseType } from '../../lib/types'
import css from './index.module.scss'

const Main = () => {
  const navigate = useNavigate()
  const aboutRef = useRef<HTMLDivElement>(null)
  const [inputValue, setInputValue] = useState('')
  const [inputHide, setInputHide] = useState(false)
  const [popularCourses, setPopularCourses] = useState<CourseType[]>([])

  useEffect(() => {
    getPopularCourses().then(setPopularCourses)
  }, [])

  const handleSend = () => {
    if (inputValue.trim()) {
      localStorage.setItem('chatInput', inputValue)
      setInputHide(true)
      setTimeout(() => {
        navigate(getChatRoute())
      }, 400)
    }
  }

  return (
    <>
      <div className={css.banner}>
        <h1 className={css.additionalTitle}>Развивайся, двигайся, учись</h1>
        <h1 className={css.additionalTitle}>
          со <span className={css.title}>SkillsNavigator</span>
        </h1>
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSend={handleSend}
          className={inputHide ? css.inputHide : ''}
        />
        <MoreButton onClick={() => aboutRef.current?.scrollIntoView({ behavior: 'smooth' })} />
      </div>

      <div className={css.page} ref={aboutRef}>
        <div className={css.aboutSection}>
          <div className={css.section1}>
            <img src={roadmapMockup} alt="" className={css.roadmapMockup} />
            <div className={css.aboutText}>
              <h3>Начни свой путь уже сегодня</h3>
              <p>
                Выбери свой путь и забудь о бесконечном поиске курсов. <strong>SkillsNavigator</strong> подберёт для
                тебя персональный образовательный <strong>roadmap с лучшими ресурсами</strong> и шагами, которые
                действительно приведут к результату.
              </p>
            </div>
          </div>

          <div className={css.forWhoText}>
            <h3>Для кого?</h3>
            <p>
              SkillsNavigator поможет всем, кто хочет <strong>расти и развиваться</strong>, но не знает, с чего начать.
              Если задумываешься о смене профессии, повышении квалификации или просто ищешь{' '}
              <strong>осознанный путь</strong> в обучении — этот сервис для тебя, чтобы не теряться в море курсов и
              составить чёткий план действий, <strong>независимо от того, на каком ты этапе.</strong>
            </p>
          </div>
        </div>

        {popularCourses.length !== 0 && <div className={css.divider} />}

        {popularCourses.length !== 0 && (
          <div className={css.coursesSection}>
            <h2 className={css.coursesTitle}>Популярные курсы</h2>
            <p className={css.additionalText}>Если хочешь попробовать что-то новое</p>

            <div className={css.courses}>
              {popularCourses.map((course) => (
                <Card {...course} key={course.id} />
              ))}
            </div>
          </div>
        )}
      </div>

      <div className={css.bgGradient}>
        <h2 className={css.coursesTitle}>
          SkillsNavigator <span className={css.additionalFont}>поможет</span>
        </h2>

        <div className={css.thoughtsSection}>
          <p>
            Если не знаешь, с чего начать — куда двигаться и какие курсы подойдут —{' '}
            <strong>SkillsNavigator подскажет путь</strong>. Он проанализирует твои цели, уровеньи составит{' '}
            <strong>персональный план</strong> развитияс подходящими ресурсами. Будь то смена деятельности или рост в
            текущей сфере. <strong>Всё просто:</strong> ставишь цель, а SkillsNavigator помогает к ней прийти.
          </p>
          <img src={thoughts} alt="" className={css.thoughtsImage} />
        </div>
      </div>

      <div className={css.page} id={css.callToAction}>
        <h2 className={css.coursesTitle}>Найди свой путь с SkillsNavigator</h2>
        <p className={css.additionalText}>Получи чёткий план действий — от цели до результата</p>
        <button className={css.ctaButton} onClick={() => navigate(getChatRoute())}>
          Начать свой путь
          <img src={arrowRight} alt="" className={css.arrowIcon} />
        </button>
      </div>
    </>
  )
}
export default Main
