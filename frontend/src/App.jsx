import { Outlet } from 'react-router-dom'

import Navbar from './components/layout/Navbar.jsx'

function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="page-container">
        <Outlet />
      </main>
    </div>
  )
}

export default App
