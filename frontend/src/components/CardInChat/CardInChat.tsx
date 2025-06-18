import { useState } from 'react'
import { Rating } from '../'
import { CardType } from '../../lib/types'
import people from '/assets/people.png'
import clock from '/assets/clock.png'
import gotoIcon from '/assets/gotoIconBlue.png'
import css from './index.module.scss'

const level = {
  easy: 'Лёгкий',
  medium: 'Средний',
  hard: 'Сложный',
}

type Props = CardType & { index?: number }

const CardInChat: React.FC<Props> = ({
  title,
  cover_url,
  duration,
  difficulty,
  price,
  authors,
  pupils_num,
  rating,
  url,
  index, // индекс карточки (начиная с 0)
}) => {
  const [hovered, setHovered] = useState(false)

  return (
    <div
      className={css.card}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={() => window.open(url, '_blank', 'noopener,noreferrer')}
    >
      {/* Индекс на фоне */}
      {typeof index === 'number' && (
        <span className={css.bgIndex}>{index + 1}</span>
      )}
      <div>
        <div className={css.topSection}>
          <img src={cover_url} alt="" className={css.image} />
          <div className={css.infoSection}>
            <Rating rating={rating} hovered={hovered} small />
            <div className={css.difficulty}>{level[difficulty]}</div>
            <div className={css.durationAndPupils}>
              <div className={css.info}>
                <img src={clock} alt="" className={css.icon} />
                {duration} ч
              </div>
              <div className={css.info}>
                <img src={people} alt="" className={css.icon} />
                {pupils_num}
              </div>
            </div>
          </div>
        </div>

        <p className={css.title}>{title}</p>
        <div className={css.authors}>
          {authors.map((author, index) => (
            <span key={index} className={css.author}>
              {author}
              {index < authors.length - 1 && ', '}
            </span>
          ))}
        </div>
      </div>

      <div className={css.bottomSection}>
        <p className={css.price}>{price} руб.</p>
        <button className={css.gotoButton} onClick={() => window.open(url, '_blank', 'noopener,noreferrer')}>
          <img src={gotoIcon} alt="" className={css.gotoIcon} />
        </button>
      </div>
    </div>
  )
}
export default CardInChat