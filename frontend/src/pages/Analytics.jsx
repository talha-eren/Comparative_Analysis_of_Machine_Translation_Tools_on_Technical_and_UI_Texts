import { useState, useEffect } from 'react'
import { getResultsSummary } from '../services/api'
import BarChart from '../components/charts/BarChart'
import RadarChart from '../components/charts/RadarChart'

function Analytics() {
  const [summary, setSummary] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  
  useEffect(() => {
    loadSummary()
  }, [])
  
  const loadSummary = async () => {
    setIsLoading(true)
    try {
      const data = await getResultsSummary()
      setSummary(data)
    } catch (error) {
      console.error('Analiz verileri yüklenemedi:', error)
    } finally {
      setIsLoading(false)
    }
  }
  
  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }
  
  if (!summary || !summary.average_scores) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card text-center py-12">
          <p className="text-xl text-gray-600">Henüz analiz verisi yok</p>
        </div>
      </div>
    )
  }
  
  const getMetricData = (metric) => {
    const data = {}
    Object.entries(summary.average_scores).forEach(([tool, scores]) => {
      data[tool] = scores[metric] || 0
    })
    return data
  }
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Sonuçlar ve Analiz</h1>
      
      {/* Doğruluk Özeti */}
      <div className="card mb-8 bg-gradient-to-r from-blue-50 to-purple-50">
        <h2 className="text-2xl font-semibold mb-6">📊 Genel Doğruluk Oranları</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {Object.entries(summary.average_scores || {}).map(([tool, scores]) => {
            // Ortalama doğruluk hesapla
            const avgScore = (
              (scores.bleu || 0) + 
              (scores.meteor || 0) + 
              (scores.chrf || 0) + 
              (1 - (scores.ter || 0))
            ) / 4
            const accuracy = (avgScore * 100).toFixed(1)
            
            const toolName = tool === 'google' ? 'Google' : 
                           tool === 'deepl' ? 'DeepL' : 
                           tool === 'microsoft' ? 'Microsoft' : 'Amazon'
            
            return (
              <div key={tool} className="text-center p-6 bg-white rounded-lg shadow">
                <div className="text-sm text-gray-600 mb-2">{toolName}</div>
                <div className="text-5xl font-bold text-blue-600 mb-2">{accuracy}%</div>
                <div className="text-xs text-gray-500">Ortalama Doğruluk</div>
              </div>
            )
          })}
        </div>
      </div>
      
      {/* Detaylı Metrikler */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-6">📈 Detaylı Metrik Skorları</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <BarChart
            data={getMetricData('bleu')}
            title="BLEU Skorları (Yüksek = İyi)"
            metric="BLEU"
          />
          <BarChart
            data={getMetricData('meteor')}
            title="METEOR Skorları (Yüksek = İyi)"
            metric="METEOR"
          />
        </div>
      </div>
      
      {/* Çok Boyutlu Karşılaştırma */}
      <div className="card mb-8">
        <RadarChart
          data={summary.average_scores}
          title="Çok Boyutlu Performans Karşılaştırması"
        />
      </div>
      
      {/* Bulgular */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">🎯 Önemli Bulgular</h2>
        
        <div className="space-y-4">
          <div className="p-4 bg-green-50 border-l-4 border-green-500 rounded">
            <p className="font-semibold text-green-900 mb-1">✅ En İyi Araç</p>
            <p className="text-green-800">
              <strong>{summary.best_tool}</strong> en yüksek BLEU skorunu aldı: <strong>{(summary.best_bleu_score * 100)?.toFixed(1)}%</strong> doğruluk
            </p>
          </div>
          
          <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
            <p className="font-semibold text-blue-900 mb-1">📊 Test Kapsamı</p>
            <p className="text-blue-800">
              Toplam <strong>{summary.total_translations?.toLocaleString()}</strong> çeviri test edildi
            </p>
          </div>
          
          <div className="p-4 bg-purple-50 border-l-4 border-purple-500 rounded">
            <p className="font-semibold text-purple-900 mb-1">📝 Değerlendirme</p>
            <p className="text-purple-800">
              Tüm çeviriler <strong>profesyonel referans çevirilerle</strong> karşılaştırıldı. 
              Skorlar BLEU, METEOR, chrF++ ve TER metriklerine göre hesaplandı.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics
