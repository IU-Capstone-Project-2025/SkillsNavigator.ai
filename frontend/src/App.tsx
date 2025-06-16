import './styles/global.scss'
import './styles/typography.scss'
import { MantineProvider } from '@mantine/core'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { Header } from './components'
import ScrollResetProvider from './lib/ScrollResetProvider'
import TextFormatProvider from './lib/TextFormatProvider'
import * as routes from './lib/routes'
import { Main } from './pages'
import * as themes from './styles/themes'

const Layout = () => {
  return (
    <>
      <Header />
      <ScrollResetProvider>
        <Routes>
          <Route path={routes.getMainRoute()} element={<Main />} />
        </Routes>
      </ScrollResetProvider>
    </>
  )
}

function App() {
  return (
    <MantineProvider theme={themes.mantine}>
      <TextFormatProvider>
        <BrowserRouter>
          <Layout />
        </BrowserRouter>
      </TextFormatProvider>
    </MantineProvider>
  )
}

export default App
