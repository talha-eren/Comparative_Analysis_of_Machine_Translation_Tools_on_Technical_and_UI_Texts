import { useState, useEffect } from 'react'
import { getDatasets } from '../services/api'

function DatasetExplorer() {
  const [datasets, setDatasets] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedDataset, setSelectedDataset] = useState(null)
  
  useEffect(() => {
    loadDatasets()
  }, [])
  
  const loadDatasets = async () => {
    setIsLoading(true)
    try {
      const data = await getDatasets()
      setDatasets(data)
    } catch (error) {
      console.error('Datasets could not be loaded:', error)
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
  
  if (!datasets || !datasets.datasets) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card text-center py-12">
          <p className="text-xl text-gray-600 mb-4">No datasets found</p>
          <p className="text-gray-500">Download datasets first</p>
        </div>
      </div>
    )
  }
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Dataset Explorer</h1>
      
      {/* Dataset List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {datasets.datasets.map(datasetName => {
          const stats = datasets.statistics?.[datasetName]
          
          return (
            <div
              key={datasetName}
              className="card cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => setSelectedDataset(datasetName)}
            >
              <h3 className="text-xl font-semibold mb-2 capitalize">
                {datasetName.replace('_', ' ')}
              </h3>
              
              {stats && (
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Segments:</span>
                    <span className="font-semibold">{stats.total_segments?.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Average Length:</span>
                    <span className="font-semibold">{stats.avg_length?.toFixed(1)} chars</span>
                  </div>
                  
                  {stats.categories && (
                    <div className="mt-3 pt-3 border-t">
                      <p className="text-gray-600 mb-2">Categories:</p>
                      {Object.entries(stats.categories).map(([cat, count]) => (
                        <div key={cat} className="flex justify-between text-xs">
                          <span className="text-gray-500 capitalize">{cat}:</span>
                          <span>{count}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
              
              <button className="mt-4 w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
                View
              </button>
            </div>
          )
        })}
      </div>
      
      {/* Dataset Statistics */}
      {datasets.statistics && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Overall Statistics</h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Dataset
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Segment Count
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Avg. Length
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Categories
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(datasets.statistics).map(([name, stats]) => (
                  <tr key={name} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap font-medium capitalize">
                      {name.replace('_', ' ')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {stats.total_segments?.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {stats.avg_length?.toFixed(1)} chars
                    </td>
                    <td className="px-6 py-4">
                      {stats.categories && Object.keys(stats.categories).join(', ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default DatasetExplorer
