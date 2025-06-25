import { Alert } from '@mantine/core'
import { IconInfoCircle } from '@tabler/icons-react'
import { useState } from 'react'

const ErrorMessage = () => {
  const icon = <IconInfoCircle />
  const [opened, setOpened] = useState(true)
  if (!opened) {
    return null
  }

  return (
    <Alert
      variant="light"
      color="red"
      radius="md"
      title="Упс, что-то пошло не так..."
      icon={icon}
      withCloseButton
      onClose={() => setOpened(false)}
    >
      Повторите попытку позже
    </Alert>
  )
}

export default ErrorMessage
