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
  const [loadingStage, setLoadingStage] = useState('')
  
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
    setLoadingStage('Çeviri araçları hazırlanıyor...')
    
    try {
      // Simüle edilmiş aşamalar
      setTimeout(() => setLoadingStage('Metniniz analiz ediliyor...'), 500)
      setTimeout(() => setLoadingStage('Çeviriler yapılıyor...'), 1000)
      setTimeout(() => setLoadingStage('En iyi sonuç belirleniyor...'), 1500)
      
      console.log('Çeviri isteği gönderiliyor:', {
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference
      })
      
      const data = await translateText(
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference || null
      )
      
      console.log('Çeviri yanıtı alındı:', data)
      console.log('Sonuçlar state\'e yazılıyor:', data)
      setResults(data)
    } catch (error) {
      console.error('Çeviri hatası:', error)
      console.error('Hata detayı:', error.response?.data || error.message)
      alert('Çeviri sırasında bir hata oluştu: ' + (error.response?.data?.error || error.message))
    } finally {
      setIsLoading(false)
      setLoadingStage('')
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
      
      {/* Loading Animation */}
      {isLoading && (
        <div className="card mb-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-300">
          <div className="flex flex-col items-center justify-center py-12">
            <div className="relative mb-6">
              <div className="w-20 h-20 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-2xl">🔄</div>
              </div>
            </div>
            <h3 className="text-xl font-bold text-blue-900 mb-2">
              {loadingStage || 'Çeviriler yapılıyor...'}
            </h3>
            <p className="text-blue-700">
              En iyi sonucu size sunacağız, lütfen bekleyin...
            </p>
            <div className="mt-4 flex gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
            </div>
          </div>
        </div>
      )}
      
      {/* Results Section */}
      {results && !isLoading && (
        <div>
          {/* Başarı Mesajı */}
          <div className="card mb-6 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300">
            <div className="flex items-center gap-4">
              <div className="text-5xl">✅</div>
              <div>
                <h2 className="text-2xl font-bold text-green-900">Çeviri Tamamlandı!</h2>
                <p className="text-green-700">En iyi sonuçları sizin için sıraladık.</p>
              </div>
            </div>
          </div>
          
          {/* En İyi Seçim Önerisi - ÜST KISIMDA */}
          {results && results.metrics && Object.keys(results.metrics).length > 0 && (() => {
            // En iyi aracı bul
            let bestTool = null
            let bestScore = -1
            
            Object.entries(results.metrics).forEach(([tool, metrics]) => {
              const avgScore = (
                (metrics.bleu || 0) + 
                (metrics.meteor || 0) + 
                (metrics.chrf || 0) + 
                (1 - (metrics.ter || 0))
              ) / 4
              
              if (avgScore > bestScore) {
                bestScore = avgScore
                bestTool = tool
              }
            })
            
            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator',
              amazon: 'Amazon Translate'
            }
            
            const accuracy = (bestScore * 100).toFixed(1)
            
            return (
              <div className="card mb-6 bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-300">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-6xl">🏆</div>
                  <div>
                    <h3 className="text-2xl font-bold text-amber-900">En İyi Sonuç</h3>
                    <p className="text-amber-700">Sizin için en uygun çeviri aracını belirledik</p>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="text-3xl font-bold text-amber-900 mb-1">
                        {toolNames[bestTool]}
                      </div>
                      <div className="text-lg text-gray-600">
                        <strong className="text-amber-600">{accuracy}%</strong> doğruluk oranı
                      </div>
                    </div>
                    <div className="text-7xl">🥇</div>
                  </div>
                  
                  <div className="border-t pt-4">
                    <p className="text-gray-700">
                      <strong>💡 Öneri:</strong> Bu metin türü için <strong className="text-amber-900">{toolNames[bestTool]}</strong> kullanmanızı öneriyoruz. 
                      {bestScore > 0.9 && " Çeviri kalitesi mükemmel seviyede."}
                      {bestScore > 0.7 && bestScore <= 0.9 && " Çeviri kalitesi çok iyi seviyede."}
                      {bestScore > 0.5 && bestScore <= 0.7 && " Çeviri kalitesi iyi seviyede."}
                      {bestScore <= 0.5 && " Çeviri kalitesi orta seviyede, manuel kontrol önerilir."}
                    </p>
                  </div>
                </div>
              </div>
            )
          })()}
          
          {/* Doğruluk Özeti - Sıralı */}
          {results && results.metrics && Object.keys(results.metrics).length > 0 && (() => {
            // Araçları doğruluk oranına göre sırala
            const sortedTools = [...selectedTools].sort((a, b) => {
              const scoreA = results.metrics[a] ? (
                (results.metrics[a].bleu || 0) + 
                (results.metrics[a].meteor || 0) + 
                (results.metrics[a].chrf || 0) + 
                (1 - (results.metrics[a].ter || 0))
              ) / 4 : -1
              
              const scoreB = results.metrics[b] ? (
                (results.metrics[b].bleu || 0) + 
                (results.metrics[b].meteor || 0) + 
                (results.metrics[b].chrf || 0) + 
                (1 - (results.metrics[b].ter || 0))
              ) / 4 : -1
              
              return scoreB - scoreA
            })
            
            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator',
              amazon: 'Amazon Translate'
            }
            
            const medals = ['🥇', '🥈', '🥉', '🏅']
            const colors = ['text-amber-600', 'text-gray-500', 'text-orange-600', 'text-blue-600']
            
            return (
              <div className="card mb-6 bg-blue-50 border-blue-200">
                <h3 className="text-lg font-semibold mb-4">📊 Tüm Sonuçlar (En İyiden En Kötüye)</h3>
                <div className="space-y-3">
                  {sortedTools.map((tool, index) => {
                    const metrics = results?.metrics?.[tool]
                    if (!metrics) return null
                    
                    // Ortalama doğruluk hesapla
                    const avgScore = (
                      (metrics.bleu || 0) + 
                      (metrics.meteor || 0) + 
                      (metrics.chrf || 0) + 
                      (1 - (metrics.ter || 0))
                    ) / 4
                    const accuracy = (avgScore * 100).toFixed(1)
                    
                    return (
                      <div key={tool} className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm">
                        <div className="flex items-center gap-3">
                          <div className="text-3xl">{medals[index] || '🏅'}</div>
                          <div>
                            <div className={`text-lg font-bold ${colors[index] || 'text-gray-700'}`}>
                              {toolNames[tool]}
                            </div>
                            <div className="text-sm text-gray-500">
                              Sıra: {index + 1}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-3xl font-bold ${colors[index] || 'text-gray-700'}`}>
                            {accuracy}%
                          </div>
                          <div className="text-xs text-gray-500">Doğruluk</div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })()}
          
          {/* Detaylı Çeviri Kartları */}
          {(() => {
            // Araçları doğruluk oranına göre sırala
            const sortedTools = results.metrics && Object.keys(results.metrics).length > 0
              ? [...selectedTools].sort((a, b) => {
                  const scoreA = results.metrics[a] ? (
                    (results.metrics[a].bleu || 0) + 
                    (results.metrics[a].meteor || 0) + 
                    (results.metrics[a].chrf || 0) + 
                    (1 - (results.metrics[a].ter || 0))
                  ) / 4 : -1
                  
                  const scoreB = results.metrics[b] ? (
                    (results.metrics[b].bleu || 0) + 
                    (results.metrics[b].meteor || 0) + 
                    (results.metrics[b].chrf || 0) + 
                    (1 - (results.metrics[b].ter || 0))
                  ) / 4 : -1
                  
                  return scoreB - scoreA
                })
              : selectedTools
            
            return (
              <div>
                <h3 className="text-xl font-semibold mb-4">Detaylı Çeviri Sonuçları</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {sortedTools.map(tool => (
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
            )
          })()}
        </div>
      )}
    </div>
  )
}

export default Compare
