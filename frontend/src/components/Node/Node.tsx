import { useState } from 'react'
import { Card } from '..'
import { CourseType } from '../../lib/types'
import doneImage from '/assets/doneImage.png'
import lockIcon from '/assets/lock.png'
import css from './index.module.scss'

const RING_SIZE = 100
const RING_STROKE = 9
const IMG_SIZE = 88

const Node: React.FC<{ course: CourseType; position: 'left' | 'right'; disabled?: boolean }> = ({
  course,
  position,
  disabled = false,
}) => {
  const [isHovered, setIsHovered] = useState(false)

  const radius = (RING_SIZE - RING_STROKE) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - course.progress * circumference

  return (
    <div className={css.node} style={disabled ? { opacity: 0.6 } : {}}>
      <div className={css.ringWrapper} onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>
        <svg className={css.progressRing} width={RING_SIZE} height={RING_SIZE}>
          <circle
            cx={RING_SIZE / 2}
            cy={RING_SIZE / 2}
            r={radius}
            fill="transparent"
            stroke="rgb(255, 255, 255, 0.7)"
            strokeWidth={course.progress === 1 ? 0 : RING_STROKE}
          />
          <circle
            cx={RING_SIZE / 2}
            cy={RING_SIZE / 2}
            r={radius}
            fill="transparent"
            stroke="#9FDDFF"
            strokeWidth={course.progress === 1 ? 0 : RING_STROKE}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={css.progressCircle}
            style={{ transition: 'stroke-dashoffset 0.8s ease-out' }}
            transform={`rotate(-90 ${RING_SIZE / 2} ${RING_SIZE / 2})`}
          />
        </svg>
        <img
          src={course.progress !== 1 ? course.cover_url : doneImage}
          className={css.image}
          width={IMG_SIZE}
          height={IMG_SIZE}
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: IMG_SIZE,
            height: IMG_SIZE,
            borderRadius: '50%',
            objectFit: 'cover',
          }}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          alt={course.title}
        />
        {disabled && (
          <div className={css.lockIconWrapper}>
            <img src={lockIcon} className={css.lockIcon} />
          </div>
        )}
      </div>
      {isHovered ? (
        <div className={`${css.cardWrapper} ${css[`position-${position}`]}`}>
          <Card {...course} inChat={true} />
        </div>
      ) : (
        <h5 className={`${css.label} ${css[`position-${position}`]}`}>{course.title}</h5>
      )}
    </div>
  )
}

export default Node
