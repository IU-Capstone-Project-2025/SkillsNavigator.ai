import { PayloadType, CourseType } from '../lib/types'
import { API_URL } from './env'

export async function searchCourses(payload: PayloadType): Promise<CourseType[]> {
  const res = await fetch(`${API_URL}/courses/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    throw new Error('Failed to fetch courses')
  }
  return res.json()
}

export async function getPopularCourses(): Promise<CourseType[]> {
  const res = await fetch(`${API_URL}/courses/popular`)
  if (!res.ok) {
    throw new Error('Failed to fetch popular courses')
  }
  return res.json()
}
