import { MantineProvider } from '@mantine/core'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import '@testing-library/jest-dom'
import Chat from './Chat'

jest.mock('../../api/env', () => ({
  API_URL: 'http://mocked-api',
}))

test('Chat page', async () => {
  render(
    <MemoryRouter>
      <MantineProvider>
        <Chat />
      </MantineProvider>
    </MemoryRouter>
  )
  await waitFor(() =>
    expect(screen.getByText(/Доброго времени суток! Что вы хотели бы освоить\?/i)).toBeInTheDocument()
  )
})
