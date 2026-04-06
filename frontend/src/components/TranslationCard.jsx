function TranslationCard({ tool, translation, metrics, timeTaken, isLoading }) {
  const calculateOverallScore = (metricBlock) => {
    if (!metricBlock) return null
    const total =
      (metricBlock.bleu || 0) +
      (metricBlock.meteor || 0) +
      (metricBlock.chrf || 0) +
      (metricBlock.comet || 0) +
      (1 - (metricBlock.ter || 0))
    return total / 5
  }
  const getScoreColor = (score) => {
    if (score >= 0.8) return 'text-success-600'
    if (score >= 0.6) return 'text-warning-600'
    return 'text-error-600'
  }

  const getScoreBgColor = (score) => {
    if (score >= 0.8) return 'bg-success-100'
    if (score >= 0.6) return 'bg-warning-100'
    return 'bg-error-100'
  }

  const toolColors = {
    google: 'border-blue-500',
    deepl: 'border-indigo-500',
    microsoft: 'border-cyan-500'
  }

  const toolNames = {
    google: 'Google Translate',
    deepl: 'DeepL',
    microsoft: 'Microsoft Translator'
  }

  return (
    <div className={`card border-t-4 ${toolColors[tool] || 'border-gray-500'}`}>
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          {toolNames[tool] || tool}
        </h3>
        {timeTaken !== undefined && (
          <p className="text-sm text-gray-500">{timeTaken}ms</p>
        )}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <>
          <div className="mb-4 p-4 bg-gray-50 rounded-lg min-h-[100px]">
            <p className="text-gray-800 whitespace-pre-wrap">{translation || 'Translation unavailable'}</p>
          </div>

          {metrics && (
            <div className="space-y-2">
              <div className="flex items-center justify-between rounded-lg bg-gray-50 px-3 py-2 text-sm">
                <span className="text-gray-700">Overall score</span>
                <span className="font-semibold text-gray-900">
                  {(calculateOverallScore(metrics) * 100).toFixed(1)}%
                </span>
              </div>
              <MetricBar label="BLEU" score={metrics.bleu} />
              <MetricBar label="METEOR" score={metrics.meteor} />
              <MetricBar label="chrF++" score={metrics.chrf} />
              <MetricBar label="COMET" score={metrics.comet} />
              <MetricBar label="TER" score={metrics.ter} inverse={true} />
            </div>
          )}

          {translation && (
            <button
              onClick={() => navigator.clipboard.writeText(translation)}
              className="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm"
            >
              Copy
            </button>
          )}
        </>
      )}
    </div>
  )
}

function MetricBar({ label, score, inverse = false }) {
  if (score === null || score === undefined) {
    return null
  }

  const displayScore = inverse ? (1 - score) : score
  const percentage = displayScore * 100

  const getColor = () => {
    if (displayScore >= 0.8) return 'bg-success-500'
    if (displayScore >= 0.6) return 'bg-warning-500'
    return 'bg-error-500'
  }

  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-700">{label}</span>
        <span className="font-semibold">{score.toFixed(3)}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getColor()} transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  )
}

export default TranslationCard
