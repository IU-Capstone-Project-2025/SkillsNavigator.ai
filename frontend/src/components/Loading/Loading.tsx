import css from './index.module.scss'

const Loading = () => {
  return (
    <div className={css.loading}>
      <div className={css.spinner}></div>
    </div>
  )
}

export default Loading
