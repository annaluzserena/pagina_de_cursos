import CatalogPage from '../courses/CatalogPage'
import Header from '../shared/ui/Header'

export default function App() {
  return (
    <>
      <a className="skip-link" href="#contenido">
        Saltar al contenido
      </a>
      <Header />
      <main id="contenido" className="container main">
        <CatalogPage />
      </main>
    </>
  )
}
