import { IconArrowUp } from '@tabler/icons-react'
import { useEffect, useRef } from 'react'
import styles from './index.module.scss'

type Props = {
  width?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void
  onSend?: () => void
  placeholder?: string
  className?: string
  focus?: boolean
}

const Input: React.FC<Props> = ({
  width = '60%',
  value,
  onChange,
  onSend,
  placeholder = 'Что изучить, чтобы стать...',
  className,
  focus = false,
}) => {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (focus && inputRef.current) {
      inputRef.current.focus()
    }
  }, [focus])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && onSend) {
      onSend()
    }
  }

  return (
    <div className={`${styles.root} ${className}`}>
      <div className={styles.searchBox} style={{ width }}>
        <input
          ref={inputRef}
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
