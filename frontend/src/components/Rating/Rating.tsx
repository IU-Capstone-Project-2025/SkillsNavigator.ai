import darkStar from '/assets/darkStar.png'
import darkEmptyStar from '/assets/darkEmptyStar.png'
import star from '/assets/star.png'
import emptyStar from '/assets/emptyStar.png'
import css from './index.module.scss'

type Props = {
  rating: number
  hovered?: boolean
  small?: boolean
}

const StarRating: React.FC<Props> = ({ rating, hovered, small = false }) => {
  const starSize = small ? 14 : 20

  return (
    <span className={css.stars}>
      {Array.from({ length: 5 }).map((_, i) => {
        const filled = i < rating
        return (
          <span key={i} className={css.starWrap} style={{ width: starSize, height: starSize }}>
            <img
              src={filled ? darkStar : darkEmptyStar}
              alt=""
              className={css.starIcon}
              style={{
                opacity: hovered ? 0 : 1,
                width: starSize,
                height: starSize,
              }}
            />
            <img
              src={filled ? star : emptyStar}
              alt=""
              className={css.starIcon}
              style={{
                opacity: hovered ? 1 : 0,
                position: 'absolute',
                left: 0,
                top: 0,
                width: starSize,
                height: starSize,
              }}
            />
          </span>
        )
      })}
    </span>
  )
}

export default StarRating
