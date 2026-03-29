import { useState, useEffect } from 'react'
import { startBatchTranslation, getBatchStatus, getDatasets } from '../services/api'

function BatchTest() {
  const [datasets, setDatasets] = useState([])
  const [selectedDataset, setSelectedDataset] = useState('test_set')
  const [selectedTools, setSelectedTools] = useState(['google', 'deepl', 'microsoft', 'amazon'])
  const [sampleSize, setSampleSize] = useState(1000)
  const [isRunning, setIsRunning] = useState(false)
  const [jobId, setJobId] = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState(null)
  
  useEffect(() => {
    loadDatasets()
  }, [])
  
  useEffect(() => {
    if (jobId && isRunning) {
      const interval = setInterval(checkProgress, 2000)
      return () => clearInterval(interval)
    }
  }, [jobId, isRunning])
  
  const loadDatasets = async () => {
    try {
      const data = await getDatasets()
      setDatasets(data.datasets || [])
    } catch (error) {
      console.error('Dataset\'ler yüklenemedi:', error)
    }
  }
  
  const checkProgress = async () => {
    if (!jobId) return
    
    try {
      const data = await getBatchStatus(jobId)
      setProgress(data.progress || 0)
      setStatus(data.status)
      
      if (data.status === 'completed') {
        setIsRunning(false)
        alert('Toplu test tamamlandı! Sonuçlar sayfasına gidebilirsiniz.')
      }
    } catch (error) {
      console.error('Durum kontrolü hatası:', error)
    }
  }
  
  const handleToolToggle = (toolId) => {
    setSelectedTools(prev =>
      prev.includes(toolId)
        ? prev.filter(t => t !== toolId)
        : [...prev, toolId]
    )
  }
  
  const handleStartTest = async () => {
    if (selectedTools.length === 0) {
      alert('Lütfen en az bir çeviri aracı seçin')
      return
    }
    
    setIsRunning(true)
    setProgress(0)
    
    try {
      const data = await startBatchTranslation(
        selectedDataset,
        selectedTools,
        sampleSize
      )
      
      setJobId(data.job_id)
    } catch (error) {
      console.error('Test başlatma hatası:', error)
      alert('Test başlatılamadı')
      setIsRunning(false)
    }
  }
  
  const tools = [
    { id: 'google', name: 'Google Translate' },
    { id: 'deepl', name: 'DeepL' },
    { id: 'microsoft', name: 'Microsoft Translator' },
    { id: 'amazon', name: 'Amazon Translate' }
  ]
  
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Toplu Test</h1>
      
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-6">Test Ayarları</h2>
        
        <div className="space-y-6">
          {/* Dataset Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dataset Seçimi
            </label>
            <select
              value={selectedDataset}
              onChange={(e) => setSelectedDataset(e.target.value)}
              className="input-field"
              disabled={isRunning}
            >
              {datasets.map(dataset => (
                <option key={dataset} value={dataset}>
                  {dataset.replace('_', ' ')}
                </option>
              ))}
            </select>
          </div>
          
          {/* Tools Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Çeviri Araçları
            </label>
            <div className="grid grid-cols-2 gap-3">
              {tools.map(tool => (
                <label key={tool.id} className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="checkbox"
                    checked={selectedTools.includes(tool.id)}
                    onChange={() => handleToolToggle(tool.id)}
                    disabled={isRunning}
                    className="mr-3"
                  />
                  <span>{tool.name}</span>
                </label>
              ))}
            </div>
          </div>
          
          {/* Sample Size */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Örnek Sayısı: {sampleSize}
            </label>
            <input
              type="range"
              min="100"
              max="10000"
              step="100"
              value={sampleSize}
              onChange={(e) => setSampleSize(Number(e.target.value))}
              disabled={isRunning}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>100</span>
              <span>5,000</span>
              <span>10,000</span>
            </div>
          </div>
          
          {/* Start Button */}
          <button
            onClick={handleStartTest}
            disabled={isRunning}
            className="btn-primary w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isRunning ? 'Test Çalışıyor...' : 'Testi Başlat'}
          </button>
        </div>
      </div>
      
      {/* Progress */}
      {isRunning && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">İlerleme</h2>
          
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span>Tamamlanan</span>
              <span className="font-semibold">{progress.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-primary-600 h-4 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
          
          <div className="text-sm text-gray-600">
            <p>Job ID: {jobId}</p>
            <p>Durum: {status || 'İşleniyor'}</p>
            <p>Seçilen araçlar: {selectedTools.join(', ')}</p>
            <p>Örnek sayısı: {sampleSize}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default BatchTest
