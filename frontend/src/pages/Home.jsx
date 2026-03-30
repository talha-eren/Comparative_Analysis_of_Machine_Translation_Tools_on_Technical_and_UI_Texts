import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getTranslatorsStatus } from '../services/api'
import StatCard from '../components/StatCard'
import {
  Zap,
  Database,
  BarChart3,
  FileText,
  ArrowRight,
  CheckCircle2,
  AlertCircle
} from 'lucide-react' // Lucide-react modern bir standarttır

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
      title: 'Çoklu Karşılaştırma',
      description: '4 dev motoru tek ekranda, milisaniyeler içinde yarıştırın.',
      icon: <Zap className="w-6 h-6 text-indigo-400" />,
      color: 'blue'
    },
    {
      title: 'Devasa Veri Seti',
      description: '50.000+ teknik segment ile gerçek dünya testleri.',
      icon: <Database className="w-6 h-6 text-emerald-400" />,
      color: 'emerald'
    },
    {
      title: 'Bilimsel Metrikler',
      description: 'BLEU ve TER gibi akademik standartlarla objektif skorlar.',
      icon: <BarChart3 className="w-6 h-6 text-amber-400" />,
      color: 'amber'
    },
    {
      title: 'Akıllı Raporlama',
      description: 'Hata paylarını ve başarı oranlarını grafiklerle analiz edin.',
      icon: <FileText className="w-6 h-6 text-rose-400" />,
      color: 'rose'
    }
  ]

  const tools = [
    { name: 'Google Translate', key: 'google', color: 'from-blue-600 to-blue-400' },
    { name: 'DeepL', key: 'deepl', color: 'from-slate-800 to-slate-600' },
    { name: 'Microsoft', key: 'microsoft', color: 'from-cyan-600 to-blue-500' }
  ]

  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-32 pb-20 bg-gradient-to-b from-blue-50 to-white">

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <span className="inline-block px-4 py-1.5 mb-6 text-sm font-medium tracking-wider text-indigo-600 uppercase bg-indigo-50 border border-indigo-200 rounded-full">
            v2.0 Şimdi Yayında
          </span>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-8">
            Çeviri Kalitesini <br />
            <span className="text-indigo-600">Verilerle Ölçün</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-gray-600 mb-10 leading-relaxed">
            Teknik dökümantasyon ve UI metinlerinde en iyi sonucu veren makine çeviri motorunu bilimsel metriklerle keşfedin.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/compare"
              className="group flex items-center justify-center px-8 py-4 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 transition-all shadow-lg"
            >
              Analize Başla
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              to="/analytics"
              className="px-8 py-4 bg-white text-gray-800 border-2 border-gray-300 rounded-xl font-bold hover:bg-gray-50 transition-all"
            >
              Sonuçları İncele
            </Link>
          </div>
        </div>
      </section>

      {/* Statistics Section (Bento Style) */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StatCard title="Toplam Dataset" value="50,000+" icon={<Database className="text-indigo-600" />} />
            <StatCard title="Aktif Servis" value="4" icon={<Zap className="text-amber-600" />} />
            <StatCard title="Analiz Metriği" value="5+" icon={<BarChart3 className="text-emerald-600" />} />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 bg-white">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Neden Bu Platform?</h2>
          <div className="h-1 w-20 bg-indigo-600 mx-auto rounded-full" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="group p-8 bg-white border-2 border-gray-200 rounded-3xl hover:border-indigo-500 hover:shadow-lg transition-all duration-300">
              <div className="mb-6 inline-block p-3 bg-gray-50 rounded-2xl group-hover:scale-110 transition-transform">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
              <p className="text-gray-600 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Tools Section */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-16">Desteklenen Servisler</h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {tools.map((tool) => {
              const isActive = translatorsStatus[tool.key]?.available;
              return (
                <div key={tool.key} className="relative overflow-hidden p-6 bg-white border-2 border-gray-200 rounded-2xl transition-all hover:shadow-lg hover:-translate-y-1">
                  <div className={`absolute top-0 left-0 w-1 h-full bg-gradient-to-b ${tool.color}`} />
                  <h3 className="text-lg font-bold text-gray-900 mb-4">{tool.name}</h3>
                  <div className="flex items-center gap-2">
                    {isActive ? (
                      <div className="flex items-center text-emerald-600 text-sm font-medium">
                        <CheckCircle2 className="w-4 h-4 mr-1.5" /> Aktif
                      </div>
                    ) : (
                      <div className="flex items-center text-rose-600 text-sm font-medium">
                        <AlertCircle className="w-4 h-4 mr-1.5" /> Pasif
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto bg-gradient-to-r from-indigo-600 to-violet-700 rounded-[2.5rem] p-12 text-center relative overflow-hidden shadow-2xl shadow-indigo-500/20">
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">Objektif Karşılaştırmaya Hazır mısınız?</h2>
          <p className="text-indigo-100 mb-10 text-lg max-w-xl mx-auto">
            Kendi metinlerinizi yükleyin veya hazır datasetlerimizi kullanarak en doğru çeviri motorunu hemen bulun.
          </p>
          <Link
            to="/compare"
            className="inline-block px-10 py-4 bg-white text-indigo-600 rounded-xl font-bold text-lg hover:bg-slate-100 transition-colors"
          >
            Hemen Ücretsiz Dene
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
