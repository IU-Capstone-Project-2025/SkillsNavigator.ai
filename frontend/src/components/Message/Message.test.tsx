import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import Message from './Message'

describe('Message', () => {
  it('renders user message', () => {
    render(<Message text="Привет" isUser={true} />)
    expect(screen.getByText('Привет')).toBeInTheDocument()
  })

  it('renders friend message', () => {
    render(<Message text="Здравствуйте!" isUser={false} />)
    expect(screen.getByText('Здравствуйте!')).toBeInTheDocument()
  })

  it('applies error style for error text', () => {
    render(<Message text="Упс, что-то пошло не так... Повторите попытку позже" isUser={false} />)
    expect(screen.getByTestId('errorBubble')).toBeInTheDocument()
  })
})
