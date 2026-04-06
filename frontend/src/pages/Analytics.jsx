import { Fragment, useState, useEffect } from 'react'
import { getResultsSummary, getComparisons } from '../services/api'
import BarChart from '../components/charts/BarChart'
import RadarChart from '../components/charts/RadarChart'

function Analytics() {
  const [summary, setSummary] = useState(null)
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isHistoryLoading, setIsHistoryLoading] = useState(false)
  const [expandedRowId, setExpandedRowId] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  const pageSize = 25
  const totalPages = Math.ceil(totalCount / pageSize)
  const getVisiblePages = () => {
    if (totalPages <= 7) {
      return Array.from({ length: totalPages }, (_, index) => index + 1)
    }

    if (currentPage <= 4) {
      return [1, 2, 3, 4, 5, 'ellipsis', totalPages]
    }

    if (currentPage >= totalPages - 3) {
      return [1, 'ellipsis', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages]
    }

    return [1, 'ellipsis', currentPage - 1, currentPage, currentPage + 1, 'ellipsis', totalPages]
  }

  useEffect(() => {
    loadSummary()
  }, [])

  useEffect(() => {
    loadHistory(currentPage)
  }, [currentPage])

  const loadSummary = async () => {
    setIsLoading(true)
    try {
      const summaryData = await getResultsSummary()
      setSummary(summaryData)
    } catch (error) {
      console.error('Analytics data could not be loaded:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadHistory = async (page) => {
    setIsHistoryLoading(true)
    try {
      const offset = (page - 1) * pageSize
      const historyData = await getComparisons(pageSize, offset)
      setHistory(historyData.records || [])
      setTotalCount(historyData.total || 0)
      setExpandedRowId(null)
      const nextTotalPages = Math.ceil((historyData.total || 0) / pageSize)
      if (nextTotalPages > 0 && page > nextTotalPages) {
        setCurrentPage(nextTotalPages)
      }
    } catch (error) {
      console.error('Past translations could not be loaded:', error)
    } finally {
      setIsHistoryLoading(false)
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
        <h1 className="text-3xl font-bold mb-8">Results & Analysis</h1>
        <div className="card text-center py-16 bg-gradient-to-br from-blue-50 to-indigo-50">
          <div className="text-6xl mb-6">📊</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">No Test Results Yet</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
            Run translation tests on the Compare page to see analytics.
          </p>
          <a
            href="/compare"
            className="inline-block px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
          >
            Start Translation Test
          </a>
        </div>
      </div>
    )
  }

  const getMetricDataFromScores = (scoresByTool, metric) => {
    const data = {}
    Object.entries(scoresByTool || {}).forEach(([tool, scores]) => {
      data[tool] = scores[metric] || 0
    })
    return data
  }

  const getMetricData = (metric) => {
    return getMetricDataFromScores(summary.average_scores, metric)
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

  const calculateAccuracy = (metrics) => {
    if (!metrics) return null
    const total =
      (metrics.bleu || 0) +
      (metrics.meteor || 0) +
      (metrics.chrf || 0) +
      (metrics.comet || 0) +
      (1 - (metrics.ter || 0))
    return total / 5
  }

  const getBestToolFromRow = (row) => {
    if (!row?.metrics || Object.keys(row.metrics).length === 0) {
      return {
        tool: row?.best_translator || null,
        score: row?.best_score ?? null
      }
    }

    let bestTool = null
    let bestScore = -1

    Object.entries(row.metrics).forEach(([tool, metrics]) => {
      const score = calculateAccuracy(metrics)
      if (score !== null && score > bestScore) {
        bestScore = score
        bestTool = tool
      }
    })

    return {
      tool: bestTool,
      score: bestScore >= 0 ? bestScore : null
    }
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

  const categoryLabels = {
    technical: 'Technical',
    ui: 'UI'
  }

  const categoryOrder = ['technical', 'ui']

  const categoryKeys = Object.keys(summary.category_breakdown || {})
    .filter((category) => summary.category_scores?.[category])
    .sort((a, b) => {
      const aIndex = categoryOrder.indexOf(a)
      const bIndex = categoryOrder.indexOf(b)
    if (aIndex === -1 && bIndex === -1) return a.localeCompare(b)
    if (aIndex === -1) return 1
    if (bIndex === -1) return -1
    return aIndex - bIndex
    })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Results & Analysis</h1>

      {/* Doğruluk Özeti (birden fazla kategori varsa) */}
      {categoryKeys.length > 1 && (
        <div className="card mb-8 bg-gradient-to-r from-blue-50 to-purple-50">
          <h2 className="text-2xl font-semibold mb-6">📊 Overall Accuracy Rates</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {Object.entries(summary.average_scores || {}).map(([tool, scores]) => {
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
                  <div className="text-xs text-gray-500">Average Accuracy</div>
                </div>
              )}
            )}
          </div>
        </div>
      )}

      {/* Detaylı Metrikler (birden fazla kategori varsa) */}
      {categoryKeys.length > 1 && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-6">📈 Detailed Metric Scores</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <BarChart
              data={getMetricData('bleu')}
              title="BLEU Scores (Higher = Better)"
              metric="BLEU"
            />
            <BarChart
              data={getMetricData('meteor')}
              title="METEOR Scores (Higher = Better)"
              metric="METEOR"
            />
            <BarChart
              data={getMetricData('chrf')}
              title="chrF++ Scores (Higher = Better)"
              metric="chrF++"
            />
            <BarChart
              data={getMetricData('ter')}
              title="TER Scores (Lower = Better)"
              metric="TER"
            />
            <BarChart
              data={getMetricData('comet')}
              title="COMET Scores (Higher = Better)"
              metric="COMET"
            />
          </div>
        </div>
      )}

      {/* Çok Boyutlu Karşılaştırma (birden fazla kategori varsa) */}
      {categoryKeys.length > 1 && (
        <div className="card mb-8">
          <RadarChart
            data={summary.average_scores}
            title="Multi-Dimensional Performance Comparison"
          />
        </div>
      )}

      {/* Kategori Bazlı Analiz */}
      {summary.category_scores && categoryKeys.length > 0 && (
        <div className="space-y-8 mb-8">
          <h2 className="text-2xl font-semibold">📂 Category-Based Results</h2>

          {categoryKeys.map((category) => {
            const categorySummary = summary.category_scores?.[category]
            if (!categorySummary || !categorySummary.average_scores) return null

            return (
              <div key={category} className="card">
                <h3 className="text-xl font-semibold mb-4">
                  {categoryLabels[category] || category}
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                  {Object.entries(categorySummary.average_scores || {}).map(([tool, scores]) => {
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
                      <div key={`${category}-${tool}`} className="text-center p-4 bg-white rounded-lg shadow">
                        <div className="text-sm text-gray-600 mb-2">{toolName}</div>
                        <div className="text-4xl font-bold text-blue-600 mb-2">{accuracy}%</div>
                        <div className="text-xs text-gray-500">Average Accuracy</div>
                      </div>
                    )
                  })}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <BarChart
                    data={getMetricDataFromScores(categorySummary.average_scores, 'bleu')}
                    title="BLEU Scores (Higher = Better)"
                    metric="BLEU"
                  />
                  <BarChart
                    data={getMetricDataFromScores(categorySummary.average_scores, 'meteor')}
                    title="METEOR Scores (Higher = Better)"
                    metric="METEOR"
                  />
                  <BarChart
                    data={getMetricDataFromScores(categorySummary.average_scores, 'chrf')}
                    title="chrF++ Scores (Higher = Better)"
                    metric="chrF++"
                  />
                  <BarChart
                    data={getMetricDataFromScores(categorySummary.average_scores, 'ter')}
                    title="TER Scores (Lower = Better)"
                    metric="TER"
                  />
                  <BarChart
                    data={getMetricDataFromScores(categorySummary.average_scores, 'comet')}
                    title="COMET Scores (Higher = Better)"
                    metric="COMET"
                  />
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Bulgular */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">🎯 Key Findings</h2>

        <div className="space-y-4">
          <div className="p-4 bg-green-50 border-l-4 border-green-500 rounded">
            <p className="font-semibold text-green-900 mb-1">✅ Best Tool</p>
            <p className="text-green-800">
              <strong>{summary.best_tool}</strong> received the highest BLEU score: <strong>{(summary.best_bleu_score * 100)?.toFixed(1)}%</strong> accuracy
            </p>
          </div>

          <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
            <p className="font-semibold text-blue-900 mb-1">📊 Test Coverage</p>
            <p className="text-blue-800">
              Total <strong>{summary.total_translations?.toLocaleString()}</strong> translations tested
            </p>
          </div>

          <div className="p-4 bg-purple-50 border-l-4 border-purple-500 rounded">
            <p className="font-semibold text-purple-900 mb-1">📝 Evaluation</p>
            <p className="text-purple-800">
              All translations were compared against <strong>professional reference translations</strong>.
              Scores were computed using BLEU, METEOR, chrF++, COMET, and TER.
            </p>
          </div>
        </div>
      </div>

      {/* Geçmiş Çeviriler */}
      <div className="card mt-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between mb-4">
          <h2 className="text-xl font-semibold">🗂 Past Translations (SQLite)</h2>
          <div className="flex flex-wrap items-center gap-2">
            {getVisiblePages().map((page, index) => {
              if (page === 'ellipsis') {
                return (
                  <span key={`ellipsis-${index}`} className="px-2 text-sm text-gray-500">
                    ...
                  </span>
                )
              }

              return (
                <button
                  key={`page-${page}`}
                  onClick={() => setCurrentPage(page)}
                  className={`h-9 w-9 rounded-lg border text-sm font-semibold transition-colors ${currentPage === page
                      ? 'bg-primary-600 text-white border-primary-600'
                      : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-100'
                    }`}
                >
                  {page}
                </button>
              )
            })}
          </div>
        </div>

        {isHistoryLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600"></div>
          </div>
        ) : history.length === 0 ? (
          <p className="text-gray-600">No history records found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Source Text</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Direction</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Best Tool</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
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
                        {(() => {
                          const best = getBestToolFromRow(row)
                          return (
                            <>
                              <td className="px-4 py-2 text-sm text-gray-700">
                                {getToolName(best.tool || '-') || '-'}
                              </td>
                              <td className="px-4 py-2 text-sm text-gray-700">
                                {best.score !== null && best.score !== undefined
                                  ? Number(best.score).toFixed(4)
                                  : '-'}
                              </td>
                            </>
                          )
                        })()}
                      </tr>

                      {isExpanded && (
                        <tr className="bg-blue-50">
                          <td colSpan={6} className="px-4 py-4">
                            <div className="space-y-4">
                              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                <div className="bg-white rounded-lg border border-blue-100 p-4">
                                  <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Source Text</div>
                                  <p className="text-sm text-gray-800 whitespace-pre-wrap">{sourceText || '-'}</p>
                                </div>
                                <div className="bg-white rounded-lg border border-blue-100 p-4">
                                  <div className="text-xs font-semibold text-gray-500 uppercase mb-2">Reference / Expected Translation</div>
                                  <p className="text-sm text-gray-800 whitespace-pre-wrap">{referenceText || '-'}</p>
                                </div>
                              </div>

                              <div className="bg-white rounded-lg border border-blue-100 p-4">
                                <h3 className="text-sm font-semibold text-gray-900 mb-3">Per-Tool Translation and Score Details</h3>
                                <div className="space-y-3">
                                  {Object.entries(row.translations || {}).map(([tool, translated]) => {
                                    const metric = row.metrics?.[tool] || {}
                                    return (
                                      <div key={`${row.id}-${tool}`} className="rounded border border-gray-200 p-3">
                                        <div className="flex items-center justify-between gap-2 mb-2">
                                          <div className="font-medium text-gray-900">{getToolName(tool)}</div>
                                          <div className="text-xs text-gray-500">{getDirectionLabel(row)}</div>
                                        </div>
                                        <div className="mb-2 text-sm text-gray-700">
                                          Overall score: <strong>{(calculateAccuracy(metric) * 100).toFixed(1)}%</strong>
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
                                    <p className="text-sm text-gray-600">No per-tool translation details found for this record.</p>
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
