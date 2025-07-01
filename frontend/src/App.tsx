import '@mantine/core/styles.css'
import './styles/global.scss'
import './styles/typography.scss'
import { MantineProvider } from '@mantine/core'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { useLocation } from 'react-router-dom'
import { Footer, Header } from './components'
import ScrollResetProvider from './lib/ScrollResetProvider'
import TextFormatProvider from './lib/TextFormatProvider'
import * as routes from './lib/routes'
import { Chat, Main, Roadmap } from './pages'
import { mantine } from './styles/themes'

const Layout = () => {
  const location = useLocation()
  const isChat = location.pathname === routes.getChatRoute()
  return (
    <>
      <Header />
      <ScrollResetProvider>
        <Routes>
          <Route path={routes.getMainRoute()} element={<Main />} />
          <Route path={routes.getChatRoute()} element={<Chat />} />
          <Route path={routes.getRoadmapRoute()} element={<Roadmap />} />
        </Routes>
      </ScrollResetProvider>
      {!isChat && <Footer />}
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
