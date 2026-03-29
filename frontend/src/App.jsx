import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Compare from './pages/Compare'
import Results from './pages/Results'
import DatasetExplorer from './pages/DatasetExplorer'
import BatchTest from './pages/BatchTest'
import Analytics from './pages/Analytics'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/results" element={<Results />} />
          <Route path="/datasets" element={<DatasetExplorer />} />
          <Route path="/batch-test" element={<BatchTest />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
