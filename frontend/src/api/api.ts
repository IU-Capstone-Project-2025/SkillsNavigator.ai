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

export async function getUserRoadmaps(): Promise<any[]> {
  const res = await fetch(`${API_URL}/roadmap/get-roadmaps`)
  if (!res.ok) {
    throw new Error('Failed to fetch user roadmaps')
  }
  return res.json()
}

export async function saveCoursesToRoadmap(roadmapName: string, courses: CourseType[]): Promise<any> {
  const res = await fetch(`${API_URL}/roadmap/save-courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ roadmap_name: roadmapName, courses }),
  })
  if (!res.ok) {
    throw new Error('Failed to save courses to roadmap')
  }
  return res.json()
}

export async function clearUserRoadmaps(): Promise<any> {
  const res = await fetch(`${API_URL}/roadmap/clear-roadmaps`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error('Failed to clear roadmaps')
  }
  return res.json()
}
