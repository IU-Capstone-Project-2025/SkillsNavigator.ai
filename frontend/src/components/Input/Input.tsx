import { IconArrowUp } from '@tabler/icons-react'
import styles from './index.module.scss'

const SearchBar: React.FC = () => {
  return (
    <div className={styles.root}>
      <div className={styles.searchBox}>
        <input type="text" className={styles.input} placeholder="Что изучить, чтобы стать..." />
      </div>
      <div className={styles.button}>
        <IconArrowUp className={styles.icon} />
      </div>
    </div>
  )
}

export default SearchBar
