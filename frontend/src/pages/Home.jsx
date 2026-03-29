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
    { name: 'Microsoft', key: 'microsoft', color: 'from-cyan-600 to-blue-500' },
    { name: 'Amazon', key: 'amazon', color: 'from-orange-500 to-yellow-500' }
  ]
  
  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 selection:bg-indigo-500/30">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-32 pb-20">
        {/* Arka plan ışık oyunları */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-indigo-500/20 via-transparent to-transparent -z-10" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <span className="inline-block px-4 py-1.5 mb-6 text-sm font-medium tracking-wider text-indigo-400 uppercase bg-indigo-500/10 border border-indigo-500/20 rounded-full">
            v2.0 Şimdi Yayında
          </span>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-8 bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-400">
            Çeviri Kalitesini <br /> 
            <span className="text-indigo-500">Verilerle Ölçün</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-slate-400 mb-10 leading-relaxed">
            Teknik dökümantasyon ve UI metinlerinde en iyi sonucu veren makine çeviri motorunu bilimsel metriklerle keşfedin.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/compare"
              className="group flex items-center justify-center px-8 py-4 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/25"
            >
              Analize Başla
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              to="/datasets"
              className="px-8 py-4 bg-slate-800 text-white border border-slate-700 rounded-xl font-bold hover:bg-slate-700 transition-all"
            >
              Datasetleri İncele
            </Link>
          </div>
        </div>
      </section>

      {/* Statistics Section (Bento Style) */}
      <section className="py-20 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StatCard title="Toplam Dataset" value="50,000+" icon={<Database className="text-indigo-500" />} />
            <StatCard title="Aktif Servis" value="4" icon={<Zap className="text-amber-500" />} />
            <StatCard title="Analiz Metriği" value="5+" icon={<BarChart3 className="text-emerald-500" />} />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Neden Bu Platform?</h2>
          <div className="h-1 w-20 bg-indigo-500 mx-auto rounded-full" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="group p-8 bg-slate-800/40 border border-slate-700/50 rounded-3xl hover:border-indigo-500/50 transition-all duration-300">
              <div className="mb-6 inline-block p-3 bg-slate-900 rounded-2xl group-hover:scale-110 transition-transform">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Tools Section */}
      <section className="py-24 bg-gradient-to-b from-transparent to-indigo-950/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-white mb-16">Desteklenen Servisler</h2>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {tools.map((tool) => {
              const isActive = translatorsStatus[tool.key]?.available;
              return (
                <div key={tool.key} className="relative overflow-hidden p-6 bg-slate-800/50 border border-slate-700 rounded-2xl transition-all hover:-translate-y-1">
                  <div className={`absolute top-0 left-0 w-1 h-full bg-gradient-to-b ${tool.color}`} />
                  <h3 className="text-lg font-bold text-white mb-4">{tool.name}</h3>
                  <div className="flex items-center gap-2">
                    {isActive ? (
                      <div className="flex items-center text-emerald-400 text-sm font-medium">
                        <CheckCircle2 className="w-4 h-4 mr-1.5" /> Aktif
                      </div>
                    ) : (
                      <div className="flex items-center text-rose-400 text-sm font-medium">
                        <AlertCircle className="w-4 h-4 mr-1.5" /> Kesinti
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
