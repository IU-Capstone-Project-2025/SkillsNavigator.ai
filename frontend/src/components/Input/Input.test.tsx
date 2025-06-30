import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import Input from './Input'

describe('Input', () => {
  it('renders with placeholder', () => {
    render(<Input value="" onChange={() => {}} />)
    expect(screen.getByPlaceholderText(/Что изучить/i)).toBeInTheDocument()
  })

  it('calls onChange when typing', () => {
    const handleChange = jest.fn()
    render(<Input value="" onChange={handleChange} />)
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'test' } })
    expect(handleChange).toHaveBeenCalled()
  })

  it('calls onSend on Enter', () => {
    const handleSend = jest.fn()
    render(<Input value="msg" onChange={() => {}} onSend={handleSend} />)
    fireEvent.keyDown(screen.getByRole('textbox'), { key: 'Enter' })
    expect(handleSend).toHaveBeenCalled()
  })
})