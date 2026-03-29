import { useState } from 'react'
import { translateText } from '../services/api'
import TranslationCard from '../components/TranslationCard'

function Compare() {
  const [text, setText] = useState('')
  const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('tr')
  const [category, setCategory] = useState('technical')
  const [selectedTools, setSelectedTools] = useState(['google', 'deepl', 'microsoft', 'amazon'])
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [reference, setReference] = useState('')
  
  const tools = [
    { id: 'google', name: 'Google Translate' },
    { id: 'deepl', name: 'DeepL' },
    { id: 'microsoft', name: 'Microsoft Translator' },
    { id: 'amazon', name: 'Amazon Translate' }
  ]
  
  const handleToolToggle = (toolId) => {
    setSelectedTools(prev => 
      prev.includes(toolId)
        ? prev.filter(t => t !== toolId)
        : [...prev, toolId]
    )
  }
  
  const handleTranslate = async () => {
    if (!text.trim()) {
      alert('Lütfen çevrilecek metni girin')
      return
    }
    
    if (selectedTools.length === 0) {
      alert('Lütfen en az bir çeviri aracı seçin')
      return
    }
    
    setIsLoading(true)
    setResults(null)
    
    try {
      const data = await translateText(
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference || null
      )
      
      setResults(data)
    } catch (error) {
      console.error('Çeviri hatası:', error)
      alert('Çeviri sırasında bir hata oluştu')
    } finally {
      setIsLoading(false)
    }
  }
  
  const exampleTexts = {
    technical: 'The function returns a promise that resolves when the operation completes successfully.',
    ui: 'Click here to save your changes and continue.',
    error: 'Invalid input: Please enter a valid email address.'
  }
  
  const loadExample = () => {
    setText(exampleTexts[category])
  }
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Çeviri Karşılaştırma</h1>
      
      {/* Input Section */}
      <div className="card mb-8">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Çevrilecek Metin
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="input-field h-32 resize-none"
            placeholder="Çevirmek istediğiniz metni buraya yazın..."
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Kaynak Dil
            </label>
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className="input-field"
            >
              <option value="en">İngilizce</option>
              <option value="tr">Türkçe</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hedef Dil
            </label>
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className="input-field"
            >
              <option value="tr">Türkçe</option>
              <option value="en">İngilizce</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Metin Tipi
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input-field"
            >
              <option value="technical">Teknik Dokümantasyon</option>
              <option value="ui">UI String</option>
              <option value="error">Hata Mesajı</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              &nbsp;
            </label>
            <button
              onClick={loadExample}
              className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Örnek Yükle
            </button>
          </div>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Referans Çeviri (Opsiyonel - Metrik hesaplama için)
          </label>
          <input
            type="text"
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            className="input-field"
            placeholder="Doğru çeviriyi buraya yazın..."
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Çeviri Araçları
          </label>
          <div className="flex flex-wrap gap-3">
            {tools.map(tool => (
              <label key={tool.id} className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedTools.includes(tool.id)}
                  onChange={() => handleToolToggle(tool.id)}
                  className="mr-2"
                />
                <span>{tool.name}</span>
              </label>
            ))}
          </div>
        </div>
        
        <button
          onClick={handleTranslate}
          disabled={isLoading}
          className="btn-primary w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Çevriliyor...' : 'Çevir'}
        </button>
      </div>
      
      {/* Results Section */}
      {(results || isLoading) && (
        <div>
          <h2 className="text-2xl font-bold mb-6">Çeviri Sonuçları</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {selectedTools.map(tool => (
              <TranslationCard
                key={tool}
                tool={tool}
                translation={results?.translations?.[tool]}
                metrics={results?.metrics?.[tool]}
                timeTaken={results?.time_taken_ms?.[tool]}
                isLoading={isLoading}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Compare
