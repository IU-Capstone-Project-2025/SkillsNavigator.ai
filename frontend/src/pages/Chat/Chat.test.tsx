import { MantineProvider } from '@mantine/core'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import Chat from './Chat'

jest.mock('../../api/env', () => ({
  API_URL: 'http://mocked-api'
}));

describe('Chat page', () => {
  it('renders first question', () => {
    render(
      <MantineProvider>
        <Chat />
      </MantineProvider>
    )
    expect(screen.getByText(/Доброго времени суток! Что вы хотели бы освоить\?/i)).toBeInTheDocument()
  })
})