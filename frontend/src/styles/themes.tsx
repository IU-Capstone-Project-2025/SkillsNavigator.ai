import { createTheme } from '@mantine/core'
// import checkboxClasses from '../components/CheckPolicy/index.module.scss'

export const mantine = createTheme({
  cursorType: 'pointer',
  components: {
    // Checkbox: Checkbox.extend({ classNames: checkboxClasses }),
    TextInput: {
      defaultProps: { radius: 'md' },
      classNames: { label: 'label' },
    },
    Textarea: {
      defaultProps: {
        radius: 'md',
        autosize: true,
        minRows: 2,
        maxRows: 25,
      },
      classNames: { label: 'label' },
      styles: {
        root: { width: '100%' },
        input: { width: '100%' },
      },
    },
    MultiSelect: {
      defaultProps: { radius: 'md' },
    },
    Modal: {
      styles: {
        root: { zIndex: 100000 },
      },
    },
    Button: {
      defaultProps: { color: '#0171fc' },
    },
  },
})
