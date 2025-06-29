import { MantineProvider } from '@mantine/core'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import Sidebar from './Sidebar'

const chats = [
  { id: 1, name: 'Чат 1', roadmapId: 0, chat: [] },
  { id: 2, name: 'Чат 2', roadmapId: 0, chat: [] },
]

describe('Sidebar', () => {
  it('renders chat names', () => {
    render(<MantineProvider><Sidebar chats={chats} activeChat={1} onSelect={() => {}} onNewChat={() => {}} /></MantineProvider>)
    expect(screen.getByText('Чат 1')).toBeInTheDocument()
    expect(screen.getByText('Чат 2')).toBeInTheDocument()
  })

  it('calls onSelect when chat is clicked', () => {
    const onSelect = jest.fn()
    render(<MantineProvider><Sidebar chats={chats} activeChat={1} onSelect={onSelect} onNewChat={() => {}} /></MantineProvider>)
    fireEvent.click(screen.getByText('Чат 2'))
    expect(onSelect).toHaveBeenCalledWith(2)
  })

  it('calls onNewChat when button is clicked', () => {
    const onNewChat = jest.fn()
    render(<MantineProvider><Sidebar chats={chats} activeChat={1} onSelect={() => {}} onNewChat={onNewChat} /></MantineProvider>)
    fireEvent.click(screen.getByText(/Новый чат/i))
    expect(onNewChat).toHaveBeenCalled()
  })
})