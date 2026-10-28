import { useEffect, useRef, useState } from 'react'

/** Header con menú sándwich en mobile (UX-UI §4.5, RNF-003). */
export default function Header() {
  const [open, setOpen] = useState(false)
  const toggleRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(false)
        toggleRef.current?.focus()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open])

  return (
    <header className="header">
      <div className="header__bar container">
        <a className="header__brand" href="/">
          RutaLibre
        </a>
        <button
          ref={toggleRef}
          type="button"
          className="header__toggle"
          aria-expanded={open}
          aria-controls="main-nav"
          aria-label={open ? 'Cerrar menú de navegación' : 'Abrir menú de navegación'}
          onClick={() => setOpen((v) => !v)}
        >
          <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" focusable="false">
            <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </button>
        <nav id="main-nav" className={`header__nav${open ? ' is-open' : ''}`} aria-label="Principal">
          <ul>
            <li>
              <a href="/" aria-current="page" onClick={() => setOpen(false)}>
                Catálogo
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
}
