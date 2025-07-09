import { PayloadType, CourseType } from '../lib/types'
import { API_URL } from './env'

export async function searchCourses(payload: PayloadType, chatId?: number): Promise<CourseType[]> {
  const body = chatId
    ? JSON.stringify({ ...payload, chat_id: chatId })
    : JSON.stringify(payload)

  const res = await fetch(`${API_URL}/courses/roadmaps`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body,
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

// Получить все чаты пользователя
export async function getChats() {
  const res = await fetch(`${API_URL}/chats`, { credentials: 'include' })
  if (!res.ok) {
    throw new Error('Failed to fetch chats')
  }
  const data = await res.json()
  return data
}

// Создать новый чат
export async function createChat() {
  const res = await fetch(`${API_URL}/chats`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error('Failed to create chat')
  }
  const data = await res.json()
  return data.id
}

// Сохранить сообщение в чате
export async function saveMessage(chatId: number, message: string, messageNumber: number) {
  const res = await fetch(`${API_URL}/chats/${chatId}`, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, messageNumber }),
  })
  if (!res.ok) {
    throw new Error('Failed to save message')
  }
  const data = await res.json()
  return data
}

// Получить roadmaps (GET)
export async function getRoadmaps() {
  const res = await fetch(`${API_URL}/courses/roadmaps`, { credentials: 'include' })
  if (!res.ok) {
    throw new Error('Failed to fetch roadmaps')
  }
  const data = await res.json()
  return data
}
