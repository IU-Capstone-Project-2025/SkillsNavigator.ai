import roadmapMockup from '/assets/roadmap_mockup.png'
import css from './index.module.scss'

const Main = () => {
  return (
    <>
      <div className={css.banner}>
        <h1 className={css.additionalTitle}>Развивайся, двигайся, учись</h1>
        <h1 className={css.additionalTitle}>
          с <span className={css.title}>SkillsNavigator</span>
        </h1>
      </div>

      <div className={css.page}>
        <div className={css.aboutSection}>
          <div className={css.section1}>
            <img src={roadmapMockup} alt="" className={css.roadmapMockup} />
            <div className={css.aboutText}>
              <h3>Начни свой путь уже сегодня</h3>
              <p>
                Выбери свой путь и забудь о бесконечном поиске курсов. <strong>SkillsNavigator</strong> подберёт для
                тебя персональный образовательный <strong>roadmap с лучшими ресурсами</strong> и шагами, которые
                действительно приведут к результату.{' '}
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

        <div className={css.divider} />

        <h2>Популярные курсы</h2>
        <p className={css.additionalText}>Если хочешь попробовать что-то новое</p>
      </div>
    </>
  )
}
export default Main
