import { useState } from 'react'
import { Node } from '../../components'
import { roadmaps } from '../../lib/data'
import styles from './index.module.scss'

const Roadmaps: React.FC = () => {
  const [loading, setLoading] = useState(false)

  if (loading) {
    return (
      <div className={styles.root}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.root}>
      <div className={styles.roadmap}>
        {roadmaps[0].courses.map((course, index) => (
          <Node key={index} course={course} position={index % 2 === 0 ? 'right' : 'left'} />
        ))}
      </div>
    </div>
  )
}

export default Roadmaps
