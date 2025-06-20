import arrowIcon from '/assets/arrow.png'
import { motion } from 'framer-motion'
import css from './index.module.scss'

const MoreButton = ({ onClick }: { onClick?: () => void }) => {
  return (
    <motion.div
      className={css.details}
      animate={{ y: [0, -15, 0] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
    >
      <button className={css.button} onClick={onClick}>Подробнее
        <img src={arrowIcon} alt="" className={css.icon} />
      </button>
    </motion.div>
  )
}
export default MoreButton
