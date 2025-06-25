import { createTheme } from '@mantine/core'
// import checkboxClasses from '../components/CheckPolicy/index.module.scss'

export const mantine = createTheme({
  cursorType: 'pointer',
  components: {
    Alert: {
      styles: {
        root: { padding: '20px' },
        label: { fontSize: '1.3rem', lineHeight: '1', marginBottom: '8px' },
        message: { fontSize: '1.3rem' },
        icon: { width: '18px' },
        closeButton: { scale: '1.5', cursor: 'pointer' },
      },
    },
  },
})
