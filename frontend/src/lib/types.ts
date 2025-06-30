export type PayloadType = {
  area: string
  current_level: string
  desired_skills: string
}

export type CourseType = {
  id: number
  cover_url: string
  title: string
  duration: number
  difficulty: 'easy' | 'medium' | 'hard' | null
  price: number
  pupils_num: number
  authors: string
  rating: number
  url: string
  progress: number
}

export type MessageType = {
  text: string
  isUser: boolean
}

export type ChatType = {
  id: number
  name: string
  roadmapId: number
  messages: MessageType[]
}

export type RoadmapType = {
  id: number
  status: 'current' | 'notNow' | 'done'
  name: string
  courses: CourseType[]
}
