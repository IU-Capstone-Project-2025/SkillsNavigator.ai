import React, { useEffect, useRef } from 'react'
import Typograf from 'typograf'

const tp = new Typograf({ locale: ['ru'] })

tp.enableRule('common/nbsp/afterShortWord')
tp.enableRule('ru/nbsp/afterPreposition')
tp.enableRule('ru/nbsp/afterShortWord')
tp.enableRule('ru/dash/main')
tp.enableRule('ru/punctuation/hellip')

const formatTextNodes = (element: HTMLElement) => {
  element.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li').forEach((el) => {
    if (el.childNodes.length === 1 && el.childNodes[0].nodeType === Node.TEXT_NODE) {
      const formattedText = tp.execute(el.textContent || '')
      if (formattedText !== el.textContent) {
        el.textContent = formattedText // Меняем только текст, а не innerHTML
      }
    }
  })
}

const TextFormatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) {
      return
    }

    formatTextNodes(containerRef.current)

    const observer = new MutationObserver(() => formatTextNodes(containerRef.current!))
    observer.observe(containerRef.current, { childList: true, subtree: true })

    return () => observer.disconnect()
  }, [])

  return <div ref={containerRef}>{children}</div>
}

export default TextFormatProvider
