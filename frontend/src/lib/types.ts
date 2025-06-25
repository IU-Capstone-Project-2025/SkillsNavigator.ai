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
  currency_code: string
  pupils_num: number
  authors: string
  rating: number
  url: string
  description: string
  summary: string
  target_audience: string
  acquired_skills: string
  acquired_assets: string
  title_en: string
  learning_format: string
}

export type MessageType = {
  text: string
  isUser: boolean
}
