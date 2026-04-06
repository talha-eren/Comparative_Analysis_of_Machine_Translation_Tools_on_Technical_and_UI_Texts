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
      console.error('Translator status could not be loaded:', error)
    }
  }

  const features = [
    {
      title: 'Multi-Engine Comparison',
      description: 'Compare 4 major engines on one screen in milliseconds.',
      icon: <Zap className="w-6 h-6 text-indigo-400" />,
      color: 'blue'
    },
    {
      title: 'Large Dataset',
      description: 'Real-world tests with 50,000+ technical segments.',
      icon: <Database className="w-6 h-6 text-emerald-400" />,
      color: 'emerald'
    },
    {
      title: 'Scientific Metrics',
      description: 'Objective scores using academic standards like BLEU and TER.',
      icon: <BarChart3 className="w-6 h-6 text-amber-400" />,
      color: 'amber'
    },
    {
      title: 'Smart Reporting',
      description: 'Analyze error margins and success rates with charts.',
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
            v2.0 Now Live
          </span>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-8">
            Measure Translation Quality <br />
            <span className="text-indigo-600">With Data</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg md:text-xl text-gray-600 mb-10 leading-relaxed">
            Discover the best machine translation engine for technical documentation and UI text with scientific metrics.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/compare"
              className="group flex items-center justify-center px-8 py-4 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-700 transition-all shadow-lg"
            >
              Start Analysis
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              to="/analytics"
              className="px-8 py-4 bg-white text-gray-800 border-2 border-gray-300 rounded-xl font-bold hover:bg-gray-50 transition-all"
            >
              View Results
            </Link>
          </div>
        </div>
      </section>

      {/* Statistics Section (Bento Style) */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StatCard title="Total Dataset" value="50,000+" icon={<Database className="text-indigo-600" />} />
            <StatCard title="Active Services" value="4" icon={<Zap className="text-amber-600" />} />
            <StatCard title="Analysis Metrics" value="5+" icon={<BarChart3 className="text-emerald-600" />} />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 bg-white">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Why This Platform?</h2>
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
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-16">Supported Services</h2>

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
                        <CheckCircle2 className="w-4 h-4 mr-1.5" /> Active
                      </div>
                    ) : (
                      <div className="flex items-center text-rose-600 text-sm font-medium">
                        <AlertCircle className="w-4 h-4 mr-1.5" /> Inactive
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
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">Ready for Objective Comparison?</h2>
          <p className="text-indigo-100 mb-10 text-lg max-w-xl mx-auto">
            Upload your own text or use our ready datasets to find the most accurate translation engine right away.
          </p>
          <Link
            to="/compare"
            className="inline-block px-10 py-4 bg-white text-indigo-600 rounded-xl font-bold text-lg hover:bg-slate-100 transition-colors"
          >
            Try It Free
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
