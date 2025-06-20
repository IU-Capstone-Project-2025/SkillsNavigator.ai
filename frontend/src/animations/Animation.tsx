import { useSpring, animated, SpringConfig } from '@react-spring/web'
import { useRef, useEffect, useState, ReactNode } from 'react'

type AnimatedContentProps = {
  children: ReactNode
  distance?: number
  direction?: 'vertical' | 'horizontal'
  reverse?: boolean
  config?: SpringConfig
  initialOpacity?: number
  animateOpacity?: boolean
  scale?: number
  threshold?: number
  delay?: number
}

const AnimatedContent: React.FC<AnimatedContentProps> = ({
  children,
  distance = 120,
  direction = 'vertical',
  reverse = false,
  config = { tension: 80, friction: 25 },
  initialOpacity = 0.5,
  animateOpacity = true,
  scale = 1,
  threshold = 0.1,
  delay = 0,
}) => {
  const [inView, setInView] = useState(false)
  const ref = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const element = ref.current
    if (!element) {
      return
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          observer.unobserve(element)
          setTimeout(() => {
            setInView(true)
          }, delay)
        }
      },
      { threshold }
    )

    observer.observe(element)

    return () => observer.disconnect()
  }, [threshold, delay])

  const directions: Record<'vertical' | 'horizontal', string> = {
    vertical: 'Y',
    horizontal: 'X',
  }

  const springProps = useSpring({
    from: {
      transform: `translate${directions[direction]}(${reverse ? `-${distance}px` : `${distance}px`}) scale(${scale})`,
      opacity: animateOpacity ? initialOpacity : 1,
    },
    to: inView
      ? {
          transform: `translate${directions[direction]}(0px) scale(1)`,
          opacity: 1,
        }
      : undefined,
    config,
  })

  return (
    <animated.div ref={ref} style={springProps} {...({ children } as any)}>
      {children}
    </animated.div>
  )
}

export default AnimatedContent
