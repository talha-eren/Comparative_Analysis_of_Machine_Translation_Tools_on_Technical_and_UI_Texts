import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getResultsSummary } from '../services/api'
import StatCard from '../components/StatCard'
import BarChart from '../components/charts/BarChart'
import RadarChart from '../components/charts/RadarChart'

function Results() {
  const [summary, setSummary] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedMetric, setSelectedMetric] = useState('bleu')

  useEffect(() => {
    loadSummary()
  }, [])

  const loadSummary = async () => {
    setIsLoading(true)
    try {
      const data = await getResultsSummary()
      setSummary(data)
    } catch (error) {
      console.error('Sonuçlar yüklenemedi:', error)
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
          <p className="text-xl text-gray-600 mb-4">Henüz sonuç bulunmuyor</p>
          <p className="text-gray-500 mb-6">Önce bazı çeviriler yapın veya toplu test çalıştırın</p>
          <div className="flex justify-center gap-4">
            <Link to="/compare" className="btn-primary">
              Çeviri Yap
            </Link>
            <Link to="/batch-test" className="btn-secondary">
              Toplu Test
            </Link>
          </div>
        </div>
      </div>
    )
  }

  const metrics = ['bleu', 'meteor', 'chrf', 'comet', 'ter']

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

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Toplam Çeviri"
          value={summary.total_translations?.toLocaleString() || '0'}
          icon="📝"
        />
        <StatCard
          title="En İyi Araç"
          value={summary.best_tool || '-'}
          icon="🏆"
        />
        <StatCard
          title="En Yüksek BLEU"
          value={summary.best_bleu_score?.toFixed(3) || '0.000'}
          icon="⭐"
        />
        <StatCard
          title="Test Edilen Araç"
          value={summary.available_tools?.length || 0}
          icon="🔧"
        />
      </div>

      {/* Metric Selector */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">Metrik Seçimi</h2>
        <div className="flex gap-2">
          {metrics.map(metric => (
            <button
              key={metric}
              onClick={() => setSelectedMetric(metric)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${selectedMetric === metric
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
            >
              {metric.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="card">
          <BarChart
            data={getMetricData(selectedMetric)}
            title={`${selectedMetric.toUpperCase()} Skorları Karşılaştırması`}
            metric={selectedMetric.toUpperCase()}
          />
        </div>

        <div className="card">
          <RadarChart
            data={summary.average_scores}
            title="Çok Boyutlu Metrik Karşılaştırması"
          />
        </div>
      </div>

      {/* Detailed Scores Table */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Detaylı Skorlar</h2>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Araç
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  BLEU
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  METEOR
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  chrF++
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  TER
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  COMET
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {Object.entries(summary.average_scores).map(([tool, scores]) => (
                <tr key={tool} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {tool}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getScoreClass(scores.bleu)}>
                      {scores.bleu?.toFixed(4) || '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getScoreClass(scores.meteor)}>
                      {scores.meteor?.toFixed(4) || '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getScoreClass(scores.chrf)}>
                      {scores.chrf?.toFixed(4) || '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getScoreClass(1 - (scores.ter || 0))}>
                      {scores.ter?.toFixed(4) || '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={getScoreClass(scores.comet)}>
                      {scores.comet?.toFixed(4) || '-'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Category Breakdown */}
      {summary.category_breakdown && (
        <div className="card mt-8">
          <h2 className="text-xl font-semibold mb-4">Kategori Dağılımı</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(summary.category_breakdown).map(([category, stats]) => (
              <div key={category} className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2 capitalize">
                  {category}
                </h3>
                <p className="text-2xl font-bold text-primary-600">
                  {stats.count}
                </p>
                <p className="text-sm text-gray-600">
                  {stats.percentage}% of total
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function getScoreClass(score) {
  if (!score) return 'text-gray-400'
  if (score >= 0.8) return 'text-success-600 font-semibold'
  if (score >= 0.6) return 'text-warning-600 font-semibold'
  return 'text-error-600 font-semibold'
}

export default Results
