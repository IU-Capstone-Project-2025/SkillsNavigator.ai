import { IconArrowUp } from '@tabler/icons-react'
import styles from './index.module.scss'

type Props = {
  width?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void
  onSend?: () => void
  placeholder?: string
  className?: string
}

const Input: React.FC<Props> = ({
  width = '60%',
  value,
  onChange,
  onSend,
  placeholder = 'Что изучить, чтобы стать...',
  className,
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && onSend) {
      onSend()
    }
  }

  return (
    <div className={`${styles.root} ${className}`}>
      <div className={styles.searchBox} style={{ width }}>
        <input
          type="text"
          className={styles.input}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onKeyDown={handleKeyDown}
        />
      </div>
      <div className={styles.button} onClick={onSend}>
        <IconArrowUp className={styles.icon} />
      </div>
    </div>
  )
}

export default Input
