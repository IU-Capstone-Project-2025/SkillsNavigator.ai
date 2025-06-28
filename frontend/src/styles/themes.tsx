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
    Tooltip: {
      styles: {
        tooltip: { width: 'fit-content', fontSize: '1.2rem', padding: '2px 8px', borderRadius: '6px', backgroundColor: 'rgba(0, 0, 0, 0.6)' },
      },
    },
  },
})
