export type PayloadType = {
  area: string
  current_level: string
  desired_skills: string
}

export type CardType = {
  id: number
  title: string
  pupils_num?: number
  cover_url: string
  duration: number
  difficulty: 'easy' | 'medium' | 'hard'
  price: number
  authors: string[]
  rating: 0 | 1 | 2 | 3 | 4 | 5
  url: string
}
