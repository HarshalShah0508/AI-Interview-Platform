import { Outlet } from 'react-router-dom'
import { ResumeAnalysisProvider } from './context/ResumeAnalysisContext'

function App() {
  return (
    <ResumeAnalysisProvider>
      <Outlet />
    </ResumeAnalysisProvider>
  )
}

export default App
