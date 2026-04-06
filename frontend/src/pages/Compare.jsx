import { useState, useEffect } from 'react'
import { translateText } from '../services/api'
import TranslationCard from '../components/TranslationCard'

function Compare() {
  // Load previous results from localStorage
  const [text, setText] = useState(() => {
    const saved = localStorage.getItem('compare_text')
    return saved || ''
  })
  const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('tr')
  const [category, setCategory] = useState('technical')
  const [selectedTools, setSelectedTools] = useState(['google', 'deepl', 'microsoft'])
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState(() => {
    const saved = localStorage.getItem('compare_results')
    return saved ? JSON.parse(saved) : null
  })
  const [reference, setReference] = useState(() => {
    const saved = localStorage.getItem('compare_reference')
    return saved || ''
  })
  const [loadingStage, setLoadingStage] = useState('')

  const calculateAccuracy = (metrics) => {
    if (!metrics) return -1
    const total =
      (metrics.bleu || 0) +
      (metrics.meteor || 0) +
      (metrics.chrf || 0) +
      (metrics.comet || 0) +
      (1 - (metrics.ter || 0))
    return total / 5
  }

  // Save results to localStorage
  useEffect(() => {
    if (results) {
      localStorage.setItem('compare_results', JSON.stringify(results))
      localStorage.setItem('compare_text', text)
      localStorage.setItem('compare_reference', reference)
    }
  }, [results, text, reference])

  const tools = [
    { id: 'google', name: 'Google Translate' },
    { id: 'deepl', name: 'DeepL' },
    { id: 'microsoft', name: 'Microsoft Translator' }
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
      alert('Please enter text to translate')
      return
    }

    if (selectedTools.length === 0) {
      alert('Please select at least one translator')
      return
    }

    setIsLoading(true)
    setResults(null)
    setLoadingStage('Preparing translators...')

    try {
      // Simulated stages
      setTimeout(() => setLoadingStage('Analyzing your text...'), 500)
      setTimeout(() => setLoadingStage('Generating translations...'), 1000)
      setTimeout(() => setLoadingStage('Selecting best result...'), 1500)

      console.log('Sending translation request:', {
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference,
        category
      })

      const data = await translateText(
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference || null,
        category
      )

      console.log('Translation response received:', data)
      console.log('Writing results to state:', data)
      setResults(data)
    } catch (error) {
      console.error('Translation error:', error)
      console.error('Error detail:', error.response?.data || error.message)
      alert('An error occurred during translation: ' + (error.response?.data?.error || error.message))
    } finally {
      setIsLoading(false)
      setLoadingStage('')
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Translation Comparison</h1>

      {/* Input Section */}
      <div className="card mb-8">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Text to Translate
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="input-field h-32 resize-none"
            placeholder="Enter the text you want to translate..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Source Language
            </label>
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className="input-field"
            >
              <option value="en">English</option>
              <option value="tr">Turkish</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Language
            </label>
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className="input-field"
            >
              <option value="tr">Turkish</option>
              <option value="en">English</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input-field"
            >
              <option value="technical">Technical</option>
              <option value="ui">UI</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Translators
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
          {isLoading ? 'Translating...' : 'Translate'}
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
              {loadingStage || 'Translations in progress...'}
            </h3>
            <p className="text-blue-700">
              We will deliver the best result, please wait...
            </p>
            <div className="mt-4 flex gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
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
                <h2 className="text-2xl font-bold text-green-900">Translation Complete!</h2>
                <p className="text-green-700">We ranked the best results for you.</p>
              </div>
            </div>
          </div>

          {/* En İyi Seçim Önerisi - ÜST KISIMDA */}
          {results && results.metrics && Object.keys(results.metrics).length > 0 && (() => {
            // En iyi aracı bul
            let bestTool = null
            let bestScore = -1

            Object.entries(results.metrics).forEach(([tool, metrics]) => {
              const avgScore = calculateAccuracy(metrics)

              if (avgScore > bestScore) {
                bestScore = avgScore
                bestTool = tool
              }
            })

            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator'
            }

            const accuracy = (bestScore * 100).toFixed(1)

            return (
              <div className="card mb-6 bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-300">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-6xl">🏆</div>
                  <div>
                    <h3 className="text-2xl font-bold text-amber-900">Best Result</h3>
                    <p className="text-amber-700">We identified the most suitable translator for you</p>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="text-3xl font-bold text-amber-900 mb-1">
                        {toolNames[bestTool]}
                      </div>
                      <div className="text-lg text-gray-600">
                        <strong className="text-amber-600">{accuracy}%</strong> accuracy
                      </div>
                    </div>
                    <div className="text-7xl">🥇</div>
                  </div>

                  <div className="border-t pt-4">
                    <p className="text-gray-700">
                      <strong>💡 Tip:</strong> For this text type, we recommend <strong className="text-amber-900">{toolNames[bestTool]}</strong>.
                      {bestScore > 0.9 && " Translation quality is excellent."}
                      {bestScore > 0.7 && bestScore <= 0.9 && " Translation quality is very good."}
                      {bestScore > 0.5 && bestScore <= 0.7 && " Translation quality is good."}
                      {bestScore <= 0.5 && " Translation quality is moderate; manual review is recommended."}
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
              const scoreA = results.metrics[a]
                ? calculateAccuracy(results.metrics[a])
                : -1

              const scoreB = results.metrics[b]
                ? calculateAccuracy(results.metrics[b])
                : -1

              return scoreB - scoreA
            })

            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator'
            }

            const medals = ['🥇', '🥈', '🥉', '🏅']
            const colors = ['text-amber-600', 'text-gray-500', 'text-orange-600', 'text-blue-600']

            return (
              <div className="card mb-6 bg-blue-50 border-blue-200">
                <h3 className="text-lg font-semibold mb-4">📊 All Results (Best to Worst)</h3>
                <div className="space-y-3">
                  {sortedTools.map((tool, index) => {
                    const metrics = results?.metrics?.[tool]
                    if (!metrics) return null

                    // Ortalama doğruluk hesapla
                    const avgScore = calculateAccuracy(metrics)
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
                              Rank: {index + 1}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-3xl font-bold ${colors[index] || 'text-gray-700'}`}>
                            {accuracy}%
                          </div>
                          <div className="text-xs text-gray-500">Accuracy</div>
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
                const scoreA = results.metrics[a]
                  ? calculateAccuracy(results.metrics[a])
                  : -1

                const scoreB = results.metrics[b]
                  ? calculateAccuracy(results.metrics[b])
                  : -1

                return scoreB - scoreA
              })
              : selectedTools

            return (
              <div>
                <h3 className="text-xl font-semibold mb-4">Detailed Translation Results</h3>
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
