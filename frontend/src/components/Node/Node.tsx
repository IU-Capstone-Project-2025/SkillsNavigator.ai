import { useState } from 'react'
import { Card } from '..'
import { CourseType } from '../../lib/types'
import doneImage from '/assets/doneImage.png'
import css from './index.module.scss'

const Node: React.FC<{ course: CourseType; position: 'left' | 'right' }> = ({ course, position }) => {
    const [isHovered, setIsHovered] = useState(false);
    
  return (
    <div className={css.node}>
      <img src={course.progress !== 1 ? course.cover_url : doneImage} className={css.image} 
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}/>
        {isHovered ? 
        <div className={`${css.cardWrapper} ${css[`position-${position}`]}`}>
          <Card {...course} inChat={true} />
        </div>
        :<h5 className={`${css.label} ${css[`position-${position}`]}`}>{course.title}</h5>
        }
        
    </div>
  )
}

export default Node
