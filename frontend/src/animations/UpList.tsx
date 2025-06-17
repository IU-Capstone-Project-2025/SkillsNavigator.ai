import React, { ReactNode } from 'react'
import Animation from './Animation'

type AnimatedListProps = {
  children: ReactNode
}

const UpList: React.FC<AnimatedListProps> = ({ children }) => {
  return (
    <>
      {React.Children.map(children, (child, index) =>
        child ? (
          <Animation
            key={`animation-${index}`}
            distance={60}
            direction="vertical"
            config={{ tension: 50, friction: 25 }}
            initialOpacity={0}
            animateOpacity={false}
            scale={1}
            threshold={0.1}
            delay={80 * index}
          >
            {child}
          </Animation>
        ) : null
      )}
    </>
  )
}

export default UpList
