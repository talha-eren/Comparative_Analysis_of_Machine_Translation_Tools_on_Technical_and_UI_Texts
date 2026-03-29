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
      <h1 className="text-3xl font-bold mb-8">Detaylı Analiz</h1>
      
      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="card">
          <BarChart
            data={getMetricData('bleu')}
            title="BLEU Skorları"
            metric="BLEU"
          />
        </div>
        
        <div className="card">
          <BarChart
            data={getMetricData('meteor')}
            title="METEOR Skorları"
            metric="METEOR"
          />
        </div>
        
        <div className="card">
          <BarChart
            data={getMetricData('chrf')}
            title="chrF++ Skorları"
            metric="chrF++"
          />
        </div>
        
        <div className="card">
          <BarChart
            data={getMetricData('ter')}
            title="TER Skorları (Düşük = İyi)"
            metric="TER"
          />
        </div>
      </div>
      
      {/* Radar Chart */}
      <div className="card mb-8">
        <RadarChart
          data={summary.average_scores}
          title="Çok Boyutlu Performans Karşılaştırması"
        />
      </div>
      
      {/* Insights */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Önemli Bulgular</h2>
        
        <div className="space-y-4">
          <div className="p-4 bg-success-50 border-l-4 border-success-500 rounded">
            <p className="font-semibold text-success-900 mb-1">En İyi Performans</p>
            <p className="text-success-800">
              {summary.best_tool} en yüksek BLEU skorunu aldı ({summary.best_bleu_score?.toFixed(3)})
            </p>
          </div>
          
          <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
            <p className="font-semibold text-blue-900 mb-1">Toplam Test</p>
            <p className="text-blue-800">
              {summary.total_translations?.toLocaleString()} çeviri {summary.available_tools?.length} farklı araçla test edildi
            </p>
          </div>
          
          {summary.category_breakdown && (
            <div className="p-4 bg-purple-50 border-l-4 border-purple-500 rounded">
              <p className="font-semibold text-purple-900 mb-1">Kategori Dağılımı</p>
              <p className="text-purple-800">
                {Object.entries(summary.category_breakdown).map(([cat, stats]) => 
                  `${cat}: ${stats.count} (${stats.percentage}%)`
                ).join(', ')}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Analytics
