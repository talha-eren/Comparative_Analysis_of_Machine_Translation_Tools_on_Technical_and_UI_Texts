import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getTranslatorsStatus } from '../services/api'
import StatCard from '../components/StatCard'

function Home() {
  const [translatorsStatus, setTranslatorsStatus] = useState({})
  
  useEffect(() => {
    loadTranslatorsStatus()
  }, [])
  
  const loadTranslatorsStatus = async () => {
    try {
      const status = await getTranslatorsStatus()
      setTranslatorsStatus(status)
    } catch (error) {
      console.error('Çeviri araçları durumu yüklenemedi:', error)
    }
  }
  
  const features = [
    {
      title: 'Çoklu Araç Karşılaştırması',
      description: '4 farklı makine çeviri aracını aynı anda test edin ve karşılaştırın',
      icon: '🔄'
    },
    {
      title: 'Kapsamlı Dataset',
      description: '50,000+ segment teknik dokümantasyon ve UI metni',
      icon: '📊'
    },
    {
      title: 'Otomatik Değerlendirme',
      description: 'BLEU, METEOR, TER, chrF++ metrikleriyle objektif analiz',
      icon: '📈'
    },
    {
      title: 'Detaylı Raporlama',
      description: 'İnteraktif grafikler ve karşılaştırma tabloları',
      icon: '📑'
    }
  ]
  
  const tools = [
    { name: 'Google Translate', key: 'google', color: 'bg-blue-500' },
    { name: 'DeepL', key: 'deepl', color: 'bg-indigo-500' },
    { name: 'Microsoft Translator', key: 'microsoft', color: 'bg-cyan-500' },
    { name: 'Amazon Translate', key: 'amazon', color: 'bg-orange-500' }
  ]
  
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">
              Makine Çeviri Araçlarının Karşılaştırmalı Analizi
            </h1>
            <p className="text-xl mb-8 text-primary-100">
              Teknik ve UI Metinlerinde İngilizce-Türkçe Çeviri Kalitesi Değerlendirmesi
            </p>
            <div className="flex justify-center gap-4">
              <Link
                to="/compare"
                className="px-8 py-3 bg-white text-primary-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Hemen Dene
              </Link>
              <Link
                to="/datasets"
                className="px-8 py-3 bg-primary-700 text-white rounded-lg font-semibold hover:bg-primary-600 transition-colors"
              >
                Dataset'leri İncele
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Özellikler</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="card text-center">
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
      
      {/* Statistics Section */}
      <div className="bg-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">İstatistikler</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard
              title="Toplam Dataset"
              value="50,000+"
              icon="📚"
            />
            <StatCard
              title="Çeviri Araçları"
              value="4"
              icon="🔧"
            />
            <StatCard
              title="Değerlendirme Metrikleri"
              value="5+"
              icon="📊"
            />
          </div>
        </div>
      </div>
      
      {/* Tools Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Karşılaştırılan Araçlar</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {tools.map((tool) => (
            <div key={tool.key} className="card">
              <div className={`w-12 h-12 ${tool.color} rounded-lg mb-4`}></div>
              <h3 className="text-xl font-semibold mb-2">{tool.name}</h3>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${
                  translatorsStatus[tool.key]?.available ? 'bg-green-500' : 'bg-red-500'
                }`}></span>
                <span className="text-sm text-gray-600">
                  {translatorsStatus[tool.key]?.available ? 'Aktif' : 'Pasif'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* CTA Section */}
      <div className="bg-primary-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Hemen Başlayın</h2>
          <p className="text-xl mb-8 text-primary-100">
            Çeviri araçlarını karşılaştırın ve en iyi sonuçları alın
          </p>
          <Link
            to="/compare"
            className="inline-block px-8 py-3 bg-white text-primary-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Karşılaştırmaya Başla
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Home
