import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const translateText = async (text, sourceLang = 'en', targetLang = 'tr', translators = ['google', 'deepl', 'microsoft', 'amazon'], reference = null) => {
  const response = await api.post('/api/translate', {
    text,
    source_lang: sourceLang,
    target_lang: targetLang,
    translators,
    reference
  })
  return response.data
}

export const startBatchTranslation = async (datasetId, translators, sampleSize) => {
  const response = await api.post('/api/batch-translate', {
    dataset_id: datasetId,
    translators,
    sample_size: sampleSize
  })
  return response.data
}

export const getBatchStatus = async (jobId) => {
  const response = await api.get(`/api/batch-translate/${jobId}`)
  return response.data
}

export const getDatasets = async () => {
  const response = await api.get('/api/datasets')
  return response.data
}

export const evaluateTranslation = async (translation, reference) => {
  const response = await api.post('/api/evaluate', {
    translation,
    reference
  })
  return response.data
}

export const getResultsSummary = async () => {
  const response = await api.get('/api/results/summary')
  return response.data
}

export const getJobResults = async (jobId) => {
  const response = await api.get(`/api/results/${jobId}`)
  return response.data
}

export const getTranslatorsStatus = async () => {
  const response = await api.get('/api/translators/status')
  return response.data
}

export const getCacheStats = async () => {
  const response = await api.get('/api/cache/stats')
  return response.data
}

export const clearCache = async () => {
  const response = await api.post('/api/cache/clear')
  return response.data
}

export default api
