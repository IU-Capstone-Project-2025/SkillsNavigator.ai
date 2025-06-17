import { IconArrowUp } from '@tabler/icons-react'
import styles from './index.module.scss'

type Props = {
  width?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void
  onSend?: () => void
  placeholder?: string
}

const Input: React.FC<Props> = ({
  width = '60%',
  value,
  onChange,
  onKeyDown,
  onSend,
  placeholder = 'Что изучить, чтобы стать...',
}) => {
  return (
    <div className={styles.root}>
      <div className={styles.searchBox} style={{ width }}>
        <input
          type="text"
          className={styles.input}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onKeyDown={onKeyDown}
        />
      </div>
      <div className={styles.button} onClick={onSend}>
        <IconArrowUp className={styles.icon} />
      </div>
    </div>
  )
}

export default Input