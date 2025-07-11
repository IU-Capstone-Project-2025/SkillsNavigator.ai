import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getRoadmaps } from '../../api/api'
import { LoginModal, Node, Sidebar } from '../../components'
import Loading from '../../components/Loading/Loading'
import { useAuth } from '../../lib/AuthProvider'
import { getChatRoute } from '../../lib/routes'
import { RoadmapType } from '../../lib/types'
import css from './index.module.scss'

type Line = {
  x1: number
  y1: number
  x2: number
  y2: number
  color: string
}

const Roadmap = () => {
  const navigate = useNavigate()
  const nodeRefs = useRef<(HTMLDivElement | null)[]>([])
  const containerRef = useRef<HTMLDivElement | null>(null)
  const [lines, setLines] = useState<Line[]>([])
  const [roadmapsState, setRoadmapsState] = useState<RoadmapType[]>([])
  const [activeRoadmap, setActiveRoadmap] = useState(-1)
  const roadmap = roadmapsState.find((r) => r.id === activeRoadmap) ?? roadmapsState[0]
  const courses = roadmap?.courses ?? []
  const [loading, setLoading] = useState(false)
  const authenticated = useAuth().authenticated
  const [openedLogin] = useState(!authenticated)

  useEffect(() => {
    const fetchRoadmaps = async () => {
      setLoading(true)
      const roadmaps = await getRoadmaps()
      setRoadmapsState(roadmaps)
      setLoading(false)
      setActiveRoadmap(roadmaps.length > 0 ? roadmaps[roadmaps.length - 1].id : -1)
    }

    fetchRoadmaps()
  }, [])

  useEffect(() => {
    const roadmapId = localStorage.getItem('roadmapId')
    if (roadmapId) {
      const id = parseInt(roadmapId, 10)
      setActiveRoadmap(id)
      localStorage.removeItem('roadmapId')
    }
  },[roadmapsState])

  const getLineColor = (progressA: number, progressB: number) => {
    if (progressA === 1 && progressB === 1) {
      return '#6BE0A4'
    }
    if ((progressA === 1 && progressB !== 1) || (progressA !== 1 && progressB === 1)) {
      return '#9FDDFF'
    }
    if ((progressA !== 0 && progressB === 0) || (progressA === 0 && progressB !== 0)) {
      return 'rgb(255, 255, 255, 0.3)'
    }
    return '#2196F3'
  }

  const recalcLines = () => {
    const newLines: Line[] = []
    const containerRect = containerRef.current?.getBoundingClientRect()
    if (!containerRect) {
      return
    }

    for (let i = 0; i < nodeRefs.current.length - 1; i++) {
      const from = nodeRefs.current[i]?.getBoundingClientRect()
      const to = nodeRefs.current[i + 1]?.getBoundingClientRect()
      const progressA = courses[i]?.progress ?? 0
      const progressB = courses[i + 1]?.progress ?? 0
      if (from && to) {
        newLines.push({
          x1: from.left + from.width / 2 - containerRect.left,
          y1: from.top + from.height / 2 - containerRect.top,
          x2: to.left + to.width / 2 - containerRect.left,
          y2: to.top + to.height / 2 - containerRect.top,
          color: getLineColor(progressA, progressB),
        })
      }
    }
    setLines(newLines)
  }

  const getCourseStates = (courses: any[]) => {
    if (courses.length === 1) {
      return [false]
    }

    const states = Array(courses.length).fill(false)

    let foundInProgress = false
    for (let i = 0; i < courses.length; i++) {
      if (foundInProgress) {
        states[i] = true
      } else if (courses[i].progress > 0 && courses[i].progress < 1) {
        foundInProgress = true
      }
    }

    const allDone = courses.every((c) => c.progress === 0 || c.progress === 1)
    if (allDone) {
      const firstNotDone = courses.findIndex((c) => c.progress !== 1)
      if (firstNotDone !== -1) {
        for (let i = firstNotDone + 1; i < courses.length; i++) {
          states[i] = true
        }
      }
    }

    return states
  }

  useEffect(() => {
    recalcLines()
    const handleResize = () => setTimeout(recalcLines, 100)
    window.addEventListener('resize', handleResize)
    window.addEventListener('scroll', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('scroll', handleResize)
    }
  }, [courses])

  const disabledStates = getCourseStates(courses)

  const sidebarRoadmaps = roadmapsState.map((r) => ({
    id: r.id,
    name: r.name,
    roadmap_id: r.id,
    messages: [],
  }))

  if (loading && authenticated) {
    return (
      <div className={css.root}>
        <Loading />
      </div>
    )
  }

  if (!authenticated) {
    return (
      <div style={{ position: 'relative' }} className={css.root}>
        <Sidebar
          chats={sidebarRoadmaps}
          activeChat={activeRoadmap}
          onSelect={setActiveRoadmap}
          onNewChat={() => navigate(getChatRoute())}
          isRoadmap
          roadmaps={roadmapsState}
          onToggleStatus={(id) => {
            setRoadmapsState((prev) =>
              prev.map((r) => (r.id === id ? { ...r, status: r.status === 'current' ? 'notNow' : 'current' } : r))
            )
          }}
        />
        <LoginModal opened={openedLogin} onClose={() => {}} withClose={false} />
      </div>
    )
  } else {
    return (
      <div ref={containerRef} style={{ position: 'relative' }} className={css.root}>
        <Sidebar
          chats={sidebarRoadmaps}
          activeChat={activeRoadmap}
          onSelect={setActiveRoadmap}
          onNewChat={() => navigate(getChatRoute())}
          isRoadmap
          roadmaps={roadmapsState}
          onToggleStatus={(id) => {
            setRoadmapsState((prev) =>
              prev.map((r) => (r.id === id ? { ...r, status: r.status === 'current' ? 'notNow' : 'current' } : r))
            )
          }}
        />
        <svg className={css.line}>
          <defs>
            <filter id="lineShadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="15" floodColor="#1a2644" floodOpacity="0.2" />
            </filter>
          </defs>
          {lines.map((line, idx) => (
            <line
              key={idx}
              x1={line.x1}
              y1={line.y1}
              x2={line.x2}
              y2={line.y2}
              stroke={line.color}
              strokeWidth={12}
              strokeLinecap="round"
              filter="url(#lineShadow)"
            />
          ))}
        </svg>

        <div className={css.roadmap}>
          {roadmapsState
            .find((r) => r.id === activeRoadmap)
            ?.courses.map((course, index) => (
              <div
                key={course.id}
                ref={(el) => {
                  nodeRefs.current[index] = el
                }}
                className={index % 2 === 0 ? css.nodeRight : css.nodeLeft}
              >
                <Node course={course} position={index % 2 === 0 ? 'right' : 'left'} disabled={disabledStates[index]} />
              </div>
            ))}
        </div>
      </div>
    )
  }
}

export default Roadmap
