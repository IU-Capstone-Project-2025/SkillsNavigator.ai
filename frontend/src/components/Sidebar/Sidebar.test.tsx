import { MantineProvider } from '@mantine/core'
import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import '@testing-library/jest-dom'
import Sidebar from './Sidebar'

const chats = [
  { id: 1, name: 'Чат 1', roadmapId: 0, messages: [] },
  { id: 2, name: 'Чат 2', roadmapId: 0, messages: [] },
]

describe('Sidebar', () => {
  it('renders chat names', () => {
    render(
      <MantineProvider>
        <MemoryRouter>
          <Sidebar chats={chats} activeChat={1} onSelect={() => {}} onNewChat={() => {}} />
        </MemoryRouter>
      </MantineProvider>
    )
    expect(screen.getByText('Чат 1')).toBeInTheDocument()
    expect(screen.getByText('Чат 2')).toBeInTheDocument()
  })

  it('calls onSelect when chat is clicked', () => {
    const onSelect = jest.fn()
    render(
      <MantineProvider>
        <MemoryRouter>
          <Sidebar chats={chats} activeChat={1} onSelect={onSelect} onNewChat={() => {}} />
        </MemoryRouter>
      </MantineProvider>
    )
    fireEvent.click(screen.getByText('Чат 2'))
    expect(onSelect).toHaveBeenCalledWith(2)
  })

  it('calls onNewChat when button is clicked', () => {
    const onNewChat = jest.fn()
    render(
      <MantineProvider>
        <MemoryRouter>
          <Sidebar chats={chats} activeChat={1} onSelect={() => {}} onNewChat={onNewChat} />
        </MemoryRouter>
      </MantineProvider>
    )
    fireEvent.click(screen.getByText(/Новый чат/i))
    expect(onNewChat).toHaveBeenCalled()
  })
})
