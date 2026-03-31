import { Fragment, useState, useEffect } from 'react'
import { getResultsSummary, getComparisons } from '../services/api'
import BarChart from '../components/charts/BarChart'
import RadarChart from '../components/charts/RadarChart'

function Analytics() {
  const [summary, setSummary] = useState(null)
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [expandedRowId, setExpandedRowId] = useState(null)

  useEffect(() => {
    loadSummary()
  }, [])

  const loadSummary = async () => {
    setIsLoading(true)
    try {
      const [summaryData, historyData] = await Promise.all([
        getResultsSummary(),
        getComparisons(100, 0)
      ])
      setSummary(summaryData)
      setHistory(historyData.records || [])
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

  if (!summary || !summary.average_scores || Object.keys(summary.average_scores).length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-8">Sonuçlar ve Analiz</h1>
        <div className="card text-center py-16 bg-gradient-to-br from-blue-50 to-indigo-50">
          <div className="text-6xl mb-6">📊</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Henüz Test Sonucu Yok</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
            Analiz görebilmek için önce "Karşılaştır" sayfasından çeviri testleri yapmanız gerekiyor.
          </p>
          <a
            href="/compare"
            className="inline-block px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
          >
            Çeviri Testine Başla
          </a>
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

  const getToolName = (tool) => {
    if (tool === 'google') return 'Google Translate'
    if (tool === 'deepl') return 'DeepL'
    if (tool === 'microsoft') return 'Microsoft Translator'
    return tool
  }

  const formatPercent = (value) => {
    if (value === null || value === undefined) return '-'
    return `${(Number(value) * 100).toFixed(1)}%`
  }

  const getDirectionLabel = (row) => {
    const source = (row.source_lang || 'en').toUpperCase()
    const target = (row.target_lang || 'tr').toUpperCase()
    return `${source} -> ${target}`
  }

  const getSourceText = (row) => {
    if ((row.source_lang || 'en').toLowerCase() === 'tr') {
      return row.text_tr || row.reference_text || ''
    }
    return row.text_en || ''
  }

  const getReferenceText = (row) => {
    if (row.reference_text) return row.reference_text
    if ((row.target_lang || 'tr').toLowerCase() === 'en') {
      return row.text_en || ''
    }
    return row.text_tr || ''
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
              (scores.comet || 0) +
              (1 - (scores.ter || 0))
            ) / 5
            const accuracy = (avgScore * 100).toFixed(1)

            const toolName = tool === 'google' ? 'Google' :
              tool === 'deepl' ? 'DeepL' :
                tool === 'microsoft' ? 'Microsoft' : tool

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
          <BarChart
            data={getMetricData('chrf')}
            title="chrF++ Skorları (Yüksek = İyi)"
            metric="chrF++"
          />
          <BarChart
            data={getMetricData('ter')}
            title="TER Skorları (Dusuk = Iyi)"
            metric="TER"
          />
          <BarChart
            data={getMetricData('comet')}
            title="COMET Skorları (Yüksek = İyi)"
            metric="COMET"
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
              Skorlar BLEU, METEOR, chrF++, COMET ve TER metriklerine göre hesaplandı.
            </p>
          </div>
        </div>
      </div>

      {/* Geçmiş Çeviriler */}
      <div className="card mt-8">
        <h2 className="text-xl font-semibold mb-4">🗂 Geçmiş Çeviriler (SQLite)</h2>

        {history.length === 0 ? (
          <p className="text-gray-600">Geçmiş kayıt bulunamadı.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Tarih</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Kaynak Metin</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Yön</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Kategori</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">En İyi Araç</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Skor</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {history.map((row) => {
                  const isExpanded = expandedRowId === row.id
                  const sourceText = getSourceText(row)
                  const referenceText = getReferenceText(row)

                  return (
                    <Fragment key={row.id}>
                      <tr
                        className="hover:bg-gray-50 cursor-pointer"
                        onClick={() => setExpandedRowId(isExpanded ? null : row.id)}
                      >
                        <td className="px-4 py-2 text-sm text-gray-700">
                          {row.created_at ? new Date(row.created_at * 1000).toLocaleString('tr-TR') : '-'}
                        </td>
                        <td className="px-4 py-2 text-sm text-gray-800 max-w-md truncate" title={sourceText || ''}>
                          {sourceText || '-'}
                        </td>
                        <td className="px-4 py-2 text-sm text-gray-700">{getDirectionLabel(row)}</td>
                        <td className="px-4 py-2 text-sm text-gray-700">{row.category || '-'}</td>
                        <td className="px-4 py-2 text-sm text-gray-700">{getToolName(row.best_translator || '-') || '-'}</td>
                        <td className="px-4 py-2 text-sm text-gray-700">
                          {row.best_score !== null && row.best_score !== undefined ? Number(row.best_score).toFixed(4) : '-'}
                        </td>
                      </tr>

                      {isExpanded && (
                        <tr className="bg-blue-50">
                          <td colSpan={6} className="px-4 py-4">
                            <div className="space-y-4">
                              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                <div className="bg-white rounded-lg border border-blue-100 p-4">
                                  <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Kaynak Metin</div>
                                  <p className="text-sm text-gray-800 whitespace-pre-wrap">{sourceText || '-'}</p>
                                </div>
                                <div className="bg-white rounded-lg border border-blue-100 p-4">
                                  <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Referans / Beklenen Çeviri</div>
                                  <p className="text-sm text-gray-800 whitespace-pre-wrap">{referenceText || '-'}</p>
                                </div>
                              </div>

                              <div className="bg-white rounded-lg border border-blue-100 p-4">
                                <h3 className="text-sm font-semibold text-gray-900 mb-3">Araç Bazlı Çeviri ve Skor Detayları</h3>
                                <div className="space-y-3">
                                  {Object.entries(row.translations || {}).map(([tool, translated]) => {
                                    const metric = row.metrics?.[tool] || {}
                                    return (
                                      <div key={`${row.id}-${tool}`} className="rounded border border-gray-200 p-3">
                                        <div className="flex items-center justify-between gap-2 mb-2">
                                          <div className="font-medium text-gray-900">{getToolName(tool)}</div>
                                          <div className="text-xs text-gray-500">{getDirectionLabel(row)}</div>
                                        </div>
                                        <p className="text-sm text-gray-800 mb-3 whitespace-pre-wrap">{translated || '-'}</p>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                                          <div className="bg-gray-50 rounded px-2 py-1">BLEU: <strong>{formatPercent(metric.bleu)}</strong></div>
                                          <div className="bg-gray-50 rounded px-2 py-1">METEOR: <strong>{formatPercent(metric.meteor)}</strong></div>
                                          <div className="bg-gray-50 rounded px-2 py-1">chrF++: <strong>{formatPercent(metric.chrf)}</strong></div>
                                          <div className="bg-gray-50 rounded px-2 py-1">TER: <strong>{formatPercent(metric.ter)}</strong></div>
                                          <div className="bg-gray-50 rounded px-2 py-1">COMET: <strong>{formatPercent(metric.comet)}</strong></div>
                                        </div>
                                      </div>
                                    )
                                  })}

                                  {(!row.translations || Object.keys(row.translations).length === 0) && (
                                    <p className="text-sm text-gray-600">Bu kayıt için araç bazlı çeviri detayı bulunamadı.</p>
                                  )}
                                </div>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default Analytics
