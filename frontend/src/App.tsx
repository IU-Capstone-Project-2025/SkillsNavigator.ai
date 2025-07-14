import '@mantine/core/styles.css'
import './styles/global.scss'
import './styles/typography.scss'
import { MantineProvider } from '@mantine/core'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { useLocation } from 'react-router-dom'
import { UpAnimation } from './animations'
import { Footer, Header } from './components'
import TextFormatProvider from './lib/TextFormatProvider'
import * as routes from './lib/routes'
import { Chat, Main, Roadmap } from './pages'
import { mantine } from './styles/themes'

const Layout = () => {
  const location = useLocation()
  const isChat = location.pathname === routes.getChatRoute()

  if ('scrollRestoration' in window.history) {
    window.history.scrollRestoration = 'manual'
  }

  return (
    <>
      <Header />
      <Routes>
        <Route path={routes.getMainRoute()} element={<Main />} />
        <Route path={routes.getChatRoute()} element={<Chat />} />
        <Route path={routes.getRoadmapRoute()} element={<Roadmap />} />
      </Routes>
      {!isChat && (
        <UpAnimation>
          <Footer />
        </UpAnimation>
      )}
    </>
  )
}

function App() {
  return (
    <MantineProvider theme={mantine}>
      <TextFormatProvider>
        <BrowserRouter>
            <Layout />
        </BrowserRouter>
      </TextFormatProvider>
    </MantineProvider>
  )
}

export default App
