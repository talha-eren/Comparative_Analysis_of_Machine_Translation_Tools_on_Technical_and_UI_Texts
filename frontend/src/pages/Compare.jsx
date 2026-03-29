import { useState, useEffect } from 'react'
import { translateText } from '../services/api'
import TranslationCard from '../components/TranslationCard'

const METRIC_WEIGHTS = {
  bleu: 0.35,
  meteor: 0.25,
  chrf: 0.25,
  ter: 0.15
}

const computeCompositeScore = (metrics = {}) => {
  const bleu = Number(metrics.bleu ?? 0)
  const meteor = Number(metrics.meteor ?? 0)
  const chrf = Number(metrics.chrf ?? 0)
  const terAccuracy = 1 - Number(metrics.ter ?? 1)

  return (
    (bleu * METRIC_WEIGHTS.bleu) +
    (meteor * METRIC_WEIGHTS.meteor) +
    (chrf * METRIC_WEIGHTS.chrf) +
    (terAccuracy * METRIC_WEIGHTS.ter)
  )
}

const getScoreBand = (score) => {
  if (score >= 0.9) return 'mukemmel'
  if (score >= 0.75) return 'cok-iyi'
  if (score >= 0.6) return 'iyi'
  if (score >= 0.45) return 'orta'
  return 'dusuk'
}

const getAnalysisByBand = (band) => {
  if (band === 'mukemmel') {
    return 'Kalite çok yüksek. Kritik metinlerde bile küçük stil düzenlemeleri dışında ek müdahale gerektirmez.'
  }
  if (band === 'cok-iyi') {
    return 'Kalite güçlü. Yayına almadan önce terminoloji ve ton uyumu için hızlı bir son kontrol yeterli olur.'
  }
  if (band === 'iyi') {
    return 'Kalite iyi seviyede. Teknik terimler, bağlam ve noktalama için manuel inceleme önerilir.'
  }
  if (band === 'orta') {
    return 'Kalite orta seviyede. Anlam kayması veya eksik çeviri riski için cümle bazlı doğrulama yapılmalıdır.'
  }
  return 'Kalite düşük seviyede. Bu çıktı sadece taslak kabul edilmeli, yayın öncesi kapsamlı insan düzeltmesi yapılmalıdır.'
}

function Compare() {
  // localStorage'dan onceki sonuclari yukle
  const [text, setText] = useState(() => {
    const saved = localStorage.getItem('compare_text')
    return saved || ''
  })
  const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('tr')
  const [category, setCategory] = useState('technical')
  const [selectedTools, setSelectedTools] = useState(['google', 'deepl', 'microsoft', 'amazon'])
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState(() => {
    const saved = localStorage.getItem('compare_results')
    return saved ? JSON.parse(saved) : null
  })
  const [reference, setReference] = useState(() => {
    const saved = localStorage.getItem('compare_reference')
    return saved || ''
  })
  const [loadingStage, setLoadingStage] = useState('')

  // Sonuclari localStorage'a kaydet
  useEffect(() => {
    if (results) {
      localStorage.setItem('compare_results', JSON.stringify(results))
      localStorage.setItem('compare_text', text)
      localStorage.setItem('compare_reference', reference)
    }
  }, [results, text, reference])

  const tools = [
    { id: 'google', name: 'Google Translate' },
    { id: 'deepl', name: 'DeepL' },
    { id: 'microsoft', name: 'Microsoft Translator' },
    { id: 'amazon', name: 'Amazon Translate' }
  ]

  const handleToolToggle = (toolId) => {
    setSelectedTools(prev =>
      prev.includes(toolId)
        ? prev.filter(t => t !== toolId)
        : [...prev, toolId]
    )
  }

  const handleTranslate = async () => {
    if (!text.trim()) {
      alert('Lütfen çevrilecek metni girin')
      return
    }

    if (selectedTools.length === 0) {
      alert('Lütfen en az bir çeviri aracı seçin')
      return
    }

    setIsLoading(true)
    setResults(null)
    setLoadingStage('Çeviri araçları hazırlanıyor...')

    try {
      // Simüle edilmiş aşamalar
      setTimeout(() => setLoadingStage('Metniniz analiz ediliyor...'), 500)
      setTimeout(() => setLoadingStage('Çeviriler yapılıyor...'), 1000)
      setTimeout(() => setLoadingStage('En iyi sonuç belirleniyor...'), 1500)

      console.log('Çeviri isteği gönderiliyor:', {
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference
      })

      const data = await translateText(
        text,
        sourceLang,
        targetLang,
        selectedTools,
        reference || null,
        category
      )

      console.log('Çeviri yanıtı alındı:', data)
      console.log('Sonuçlar state\'e yazılıyor:', data)
      setResults(data)
    } catch (error) {
      console.error('Çeviri hatası:', error)
      console.error('Hata detayı:', error.response?.data || error.message)
      alert('Çeviri sırasında bir hata oluştu: ' + (error.response?.data?.error || error.message))
    } finally {
      setIsLoading(false)
      setLoadingStage('')
    }
  }

  const exampleTexts = [
    {
      id: 1,
      title: 'API Dokümantasyonu',
      text: 'The API endpoint accepts HTTP POST requests with JSON payloads containing authentication tokens, request parameters, and optional metadata fields. The server validates the incoming data structure, processes the business logic asynchronously using a message queue system, and returns a standardized response object with status codes, result data, and error messages if applicable. Rate limiting is enforced at 100 requests per minute per API key to prevent abuse.',
      reference: 'API uç noktası, kimlik doğrulama belirteçleri, istek parametreleri ve isteğe bağlı meta veri alanlarını içeren JSON yükleriyle HTTP POST isteklerini kabul eder. Sunucu, gelen veri yapısını doğrular, iş mantığını bir mesaj kuyruğu sistemi kullanarak eşzamansız olarak işler ve durum kodları, sonuç verileri ve varsa hata mesajlarını içeren standartlaştırılmış bir yanıt nesnesi döndürür. Kötüye kullanımı önlemek için API anahtarı başına dakikada 100 istek hız sınırlaması uygulanır.'
    },
    {
      id: 2,
      text: 'When implementing a microservices architecture, it is crucial to establish proper service discovery mechanisms, implement circuit breakers for fault tolerance, and design comprehensive monitoring solutions. Each service should maintain its own database to ensure loose coupling, communicate through well-defined APIs using REST or gRPC protocols, and handle failures gracefully with appropriate retry strategies and fallback mechanisms.',
      reference: 'Bir mikro hizmet mimarisi uygularken, uygun hizmet keşif mekanizmaları oluşturmak, hata toleransı için devre kesiciler uygulamak ve kapsamlı izleme çözümleri tasarlamak çok önemlidir. Her hizmet, gevşek bağlantıyı sağlamak için kendi veritabanını korumalı, REST veya gRPC protokollerini kullanarak iyi tanımlanmış API\'ler aracılığıyla iletişim kurmalı ve uygun yeniden deneme stratejileri ve yedek mekanizmalarla hataları zarif bir şekilde ele almalıdır.'
    },
    {
      id: 3,
      text: 'The authentication middleware intercepts incoming requests, extracts bearer tokens from authorization headers, validates them against the token store, and attaches user context to the request object. If validation fails, it returns a 401 Unauthorized response with appropriate error details. The middleware also handles token refresh logic automatically when tokens are close to expiration.',
      reference: 'Kimlik doğrulama ara yazılımı gelen istekleri yakalar, yetkilendirme başlıklarından taşıyıcı belirteçleri çıkarır, bunları belirteç deposuna karşı doğrular ve kullanıcı bağlamını istek nesnesine ekler. Doğrulama başarısız olursa, uygun hata ayrıntılarıyla 401 Yetkisiz yanıtı döndürür. Ara yazılım ayrıca belirteçlerin süresinin dolmasına yakın olduğunda belirteç yenileme mantığını otomatik olarak işler.'
    },
    {
      id: 4,
      text: 'Modern web applications leverage client-side rendering frameworks like React or Vue.js to create dynamic, responsive user interfaces. These frameworks utilize virtual DOM diffing algorithms to minimize actual DOM manipulations, implement component-based architectures for code reusability, and provide state management solutions through hooks or dedicated libraries like Redux or Vuex.',
      reference: 'Modern web uygulamaları, dinamik ve duyarlı kullanıcı arayüzleri oluşturmak için React veya Vue.js gibi istemci tarafı işleme çerçevelerinden yararlanır. Bu çerçeveler, gerçek DOM manipülasyonlarını en aza indirmek için sanal DOM karşılaştırma algoritmalarını kullanır, kod yeniden kullanılabilirliği için bileşen tabanlı mimariler uygular ve hook\'lar veya Redux veya Vuex gibi özel kütüphaneler aracılığıyla durum yönetimi çözümleri sağlar.'
    },
    {
      id: 5,
      text: 'Database optimization requires careful analysis of query patterns, proper indexing strategies, and efficient schema design. Composite indexes should be created for frequently joined columns, query execution plans must be analyzed to identify bottlenecks, and denormalization techniques may be applied selectively to improve read performance while maintaining data consistency through application-level constraints.',
      reference: 'Veritabanı optimizasyonu, sorgu desenlerinin dikkatli bir şekilde analiz edilmesini, uygun indeksleme stratejilerini ve verimli şema tasarımını gerektirir. Sık birleştirilen sütunlar için bileşik indeksler oluşturulmalı, darboğazları belirlemek için sorgu yürütme planları analiz edilmeli ve okuma performansını artırmak için seçici olarak normalleştirme teknikleri uygulanabilir, aynı zamanda uygulama düzeyinde kısıtlamalar aracılığıyla veri tutarlılığı korunmalıdır.'
    },
    {
      id: 6,
      text: 'Container orchestration platforms like Kubernetes provide automated deployment, scaling, and management of containerized applications across clusters of hosts. They handle service discovery, load balancing, rolling updates, and self-healing capabilities. Configuration is managed through declarative YAML manifests that define desired state, and the control plane continuously reconciles actual state with desired state.',
      reference: 'Kubernetes gibi konteyner orkestrasyon platformları, ana bilgisayar kümeleri arasında konteynerleştirilmiş uygulamaların otomatik dağıtımını, ölçeklendirmesini ve yönetimini sağlar. Hizmet keşfi, yük dengeleme, kademeli güncellemeler ve kendi kendini iyileştirme yeteneklerini yönetirler. Yapılandırma, istenen durumu tanımlayan bildirimsel YAML manifestoları aracılığıyla yönetilir ve kontrol düzlemi, gerçek durumu istenen durumla sürekli olarak uzlaştırır.'
    },
    {
      id: 7,
      text: 'Implementing secure authentication systems requires multiple layers of protection including password hashing with salt using algorithms like bcrypt or Argon2, secure session management with HTTP-only cookies, CSRF token validation, rate limiting on login endpoints, and multi-factor authentication options. Additionally, all sensitive operations should be logged for audit purposes and suspicious activities should trigger automated alerts.',
      reference: 'Güvenli kimlik doğrulama sistemlerinin uygulanması, bcrypt veya Argon2 gibi algoritmalar kullanılarak tuz ile şifre karması oluşturma, yalnızca HTTP tanımlama bilgileriyle güvenli oturum yönetimi, CSRF belirteci doğrulaması, giriş uç noktalarında hız sınırlaması ve çok faktörlü kimlik doğrulama seçenekleri dahil olmak üzere birden fazla koruma katmanı gerektirir. Ek olarak, tüm hassas işlemler denetim amaçlı olarak günlüğe kaydedilmeli ve şüpheli faaliyetler otomatik uyarıları tetiklemelidir.'
    },
    {
      id: 8,
      text: 'Real-time data synchronization between distributed systems can be achieved through event-driven architectures using message brokers like RabbitMQ or Apache Kafka. Events are published to topics when state changes occur, and interested services subscribe to relevant topics to receive updates. This decoupled approach enables horizontal scaling, improves fault tolerance, and allows services to process events asynchronously at their own pace.',
      reference: 'Dağıtık sistemler arasında gerçek zamanlı veri senkronizasyonu, RabbitMQ veya Apache Kafka gibi mesaj aracıları kullanılarak olay odaklı mimariler aracılığıyla sağlanabilir. Durum değişiklikleri meydana geldiğinde olaylar konulara yayınlanır ve ilgili hizmetler güncellemeleri almak için ilgili konulara abone olur. Bu ayrıştırılmış yaklaşım, yatay ölçeklendirmeyi sağlar, hata toleransını artırır ve hizmetlerin olayları kendi hızlarında eşzamansız olarak işlemesine olanak tanır.'
    },
    {
      id: 9,
      text: 'Performance optimization in web applications involves minimizing bundle sizes through code splitting and tree shaking, implementing lazy loading for routes and components, optimizing images with modern formats like WebP, utilizing browser caching strategies, and reducing the number of HTTP requests through resource bundling. Server-side rendering or static site generation can significantly improve initial page load times.',
      reference: 'Web uygulamalarında performans optimizasyonu, kod bölme ve ağaç sallama yoluyla paket boyutlarını en aza indirmeyi, rotalar ve bileşenler için tembel yükleme uygulamayı, WebP gibi modern formatlarla görüntüleri optimize etmeyi, tarayıcı önbelleğe alma stratejilerini kullanmayı ve kaynak paketleme yoluyla HTTP istek sayısını azaltmayı içerir. Sunucu tarafı işleme veya statik site oluşturma, ilk sayfa yükleme sürelerini önemli ölçüde iyileştirebilir.'
    },
    {
      id: 10,
      text: 'Continuous integration and deployment pipelines automate the software delivery process by running automated tests, performing code quality checks, building artifacts, and deploying to various environments. The pipeline should include unit tests, integration tests, security scans, and performance benchmarks. Failed builds should trigger notifications, and successful deployments to production should only occur after passing all quality gates and receiving appropriate approvals.',
      reference: 'Sürekli entegrasyon ve dağıtım hatları, otomatik testler çalıştırarak, kod kalitesi kontrolleri yaparak, yapılar oluşturarak ve çeşitli ortamlara dağıtarak yazılım teslimat sürecini otomatikleştirir. Hattın birim testlerini, entegrasyon testlerini, güvenlik taramalarını ve performans kıyaslamalarını içermesi gerekir. Başarısız derlemeler bildirimleri tetiklemeli ve üretime başarılı dağıtımlar yalnızca tüm kalite kapılarından geçtikten ve uygun onayları aldıktan sonra gerçekleşmelidir.'
    },
    {
      id: 11,
      text: 'Machine learning model deployment requires careful consideration of inference latency, throughput requirements, and resource constraints. Models can be served through REST APIs, gRPC services, or embedded directly in applications. Batch prediction is suitable for non-real-time scenarios, while online prediction with model caching and request batching optimizes latency for real-time applications. Model versioning and A/B testing capabilities are essential for safe production deployments.',
      reference: 'Makine öğrenimi modeli dağıtımı, çıkarım gecikmesi, verim gereksinimleri ve kaynak kısıtlamalarının dikkatli bir şekilde değerlendirilmesini gerektirir. Modeller REST API\'leri, gRPC hizmetleri aracılığıyla sunulabilir veya doğrudan uygulamalara gömülebilir. Toplu tahmin, gerçek zamanlı olmayan senaryolar için uygundur, model önbelleğe alma ve istek toplu işleme ile çevrimiçi tahmin, gerçek zamanlı uygulamalar için gecikmeyi optimize eder. Model sürümleme ve A/B test yetenekleri, güvenli üretim dağıtımları için gereklidir.'
    },
    {
      id: 12,
      text: 'Cloud infrastructure management involves provisioning resources through infrastructure-as-code tools like Terraform or CloudFormation, implementing auto-scaling policies based on metrics like CPU utilization and request rates, configuring load balancers for traffic distribution, setting up monitoring and alerting systems, and establishing disaster recovery procedures with regular backup schedules and tested restoration processes.',
      reference: 'Bulut altyapısı yönetimi, Terraform veya CloudFormation gibi kod olarak altyapı araçları aracılığıyla kaynakları sağlamayı, CPU kullanımı ve istek oranları gibi metriklere dayalı otomatik ölçeklendirme politikaları uygulamayı, trafik dağıtımı için yük dengeleyicileri yapılandırmayı, izleme ve uyarı sistemleri kurmayı ve düzenli yedekleme programları ve test edilmiş geri yükleme süreçleriyle felaket kurtarma prosedürleri oluşturmayı içerir.'
    }
  ]

  const [selectedExample, setSelectedExample] = useState(null)

  const loadExample = (example) => {
    setText(example.text)
    setReference(example.reference)
    setSelectedExample(example.id)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Çeviri Karşılaştırma</h1>

      {/* Input Section */}
      <div className="card mb-8">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Çevrilecek Metin
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="input-field h-32 resize-none"
            placeholder="Çevirmek istediğiniz metni buraya yazın..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📚 Örnek Metinler (Seçin ve Test Edin)
          </label>
          <select
            value={selectedExample || ''}
            onChange={(e) => {
              const example = exampleTexts.find(ex => ex.id === parseInt(e.target.value))
              if (example) loadExample(example)
            }}
            className="input-field mb-2 text-sm"
          >
            <option value="">-- Uzun Yazılımsal Metin Seçin --</option>
            {exampleTexts.map((example) => (
              <option key={example.id} value={example.id}>
                {example.title}: {example.text.substring(0, 100)}...
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Kaynak Dil
            </label>
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className="input-field"
            >
              <option value="en">İngilizce</option>
              <option value="tr">Türkçe</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hedef Dil
            </label>
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className="input-field"
            >
              <option value="tr">Türkçe</option>
              <option value="en">İngilizce</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Çeviri Araçları
          </label>
          <div className="flex flex-wrap gap-3">
            {tools.map(tool => (
              <label key={tool.id} className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedTools.includes(tool.id)}
                  onChange={() => handleToolToggle(tool.id)}
                  className="mr-2"
                />
                <span>{tool.name}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          onClick={handleTranslate}
          disabled={isLoading}
          className="btn-primary w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Çevriliyor...' : 'Çevir'}
        </button>
      </div>

      {/* Loading Animation */}
      {isLoading && (
        <div className="card mb-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-300">
          <div className="flex flex-col items-center justify-center py-12">
            <div className="relative mb-6">
              <div className="w-20 h-20 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-2xl">🔄</div>
              </div>
            </div>
            <h3 className="text-xl font-bold text-blue-900 mb-2">
              {loadingStage || 'Çeviriler yapılıyor...'}
            </h3>
            <p className="text-blue-700">
              En iyi sonucu size sunacağız, lütfen bekleyin...
            </p>
            <div className="mt-4 flex gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {results && !isLoading && (
        <div>
          {/* Başarı Mesajı */}
          <div className="card mb-6 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300">
            <div className="flex items-center gap-4">
              <div className="text-5xl">✅</div>
              <div>
                <h2 className="text-2xl font-bold text-green-900">Çeviri Tamamlandı!</h2>
                <p className="text-green-700">En iyi sonuçları sizin için sıraladık.</p>
              </div>
            </div>
          </div>

          {/* En İyi Seçim Önerisi - ÜST KISIMDA */}
          {results && results.metrics && Object.keys(results.metrics).length > 0 && (() => {
            const rankedTools = Object.entries(results.metrics)
              .map(([tool, metrics]) => ({
                tool,
                metrics,
                score: computeCompositeScore(metrics)
              }))
              .sort((a, b) => b.score - a.score)

            const best = rankedTools[0]
            const second = rankedTools[1] || null
            const bestTool = best?.tool
            const bestScore = best?.score ?? 0

            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator',
              amazon: 'Amazon Translate'
            }

            const accuracy = (bestScore * 100).toFixed(1)
            const margin = second ? ((best.score - second.score) * 100).toFixed(1) : null
            const band = getScoreBand(bestScore)
            const analysisText = getAnalysisByBand(band)
            const isEstimated = best?.metrics?.metric_mode === 'estimated_no_reference'

            return (
              <div className="card mb-6 bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-300">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-6xl">🏆</div>
                  <div>
                    <h3 className="text-2xl font-bold text-amber-900">En İyi Sonuç</h3>
                    <p className="text-amber-700">Sizin için en uygun çeviri aracını belirledik</p>
                  </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-md">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="text-3xl font-bold text-amber-900 mb-1">
                        {toolNames[bestTool]}
                      </div>
                      <div className="text-lg text-gray-600">
                        <strong className="text-amber-600">{accuracy}%</strong> doğruluk oranı
                      </div>
                    </div>
                    <div className="text-7xl">🥇</div>
                  </div>

                  <div className="border-t pt-4">
                    <p className="text-gray-700 mb-2">
                      <strong>💡 Öneri:</strong> Bu metin türü için <strong className="text-amber-900">{toolNames[bestTool]}</strong> öncelikli seçenek olarak öne çıkıyor.
                    </p>
                    <p className="text-sm text-gray-700 mb-2">
                      Ağırlıklı kalite skoru: <strong>{accuracy}%</strong>. {analysisText}
                    </p>
                    {isEstimated && (
                      <p className="text-xs text-amber-800 mb-2">
                        Bu sonuç referans metin olmadığı için tahmini (no-reference) kalite metrikleriyle hesaplandı.
                      </p>
                    )}
                    <p className="text-sm text-gray-700 mb-2">
                      Metrik kırılımı: BLEU <strong>{((best.metrics?.bleu || 0) * 100).toFixed(1)}%</strong>,
                      METEOR <strong>{((best.metrics?.meteor || 0) * 100).toFixed(1)}%</strong>,
                      chrF++ <strong>{((best.metrics?.chrf || 0) * 100).toFixed(1)}%</strong>,
                      TER doğruluğu <strong>{((1 - (best.metrics?.ter || 0)) * 100).toFixed(1)}%</strong>.
                    </p>
                    {best.metrics?.round_trip_consistency !== undefined && best.metrics?.round_trip_consistency !== null && (
                      <p className="text-sm text-gray-700 mb-2">
                        Round-trip tutarlılığı: <strong>{(best.metrics.round_trip_consistency * 100).toFixed(1)}%</strong>
                      </p>
                    )}
                    {margin !== null && (
                      <p className="text-sm text-gray-700">
                        İkinci sıradaki <strong>{toolNames[second.tool]}</strong> ile fark: <strong>{margin}%</strong>.
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )
          })()}

          {/* Doğruluk Özeti - Sıralı */}
          {results && results.metrics && Object.keys(results.metrics).length > 0 && (() => {
            // Araçları doğruluk oranına göre sırala
            const sortedTools = [...selectedTools].sort((a, b) => {
              const scoreA = results.metrics[a] ? computeCompositeScore(results.metrics[a]) : -1
              const scoreB = results.metrics[b] ? computeCompositeScore(results.metrics[b]) : -1

              return scoreB - scoreA
            })

            const toolNames = {
              google: 'Google Translate',
              deepl: 'DeepL',
              microsoft: 'Microsoft Translator',
              amazon: 'Amazon Translate'
            }

            const medals = ['🥇', '🥈', '🥉', '🏅']
            const colors = ['text-amber-600', 'text-gray-500', 'text-orange-600', 'text-blue-600']

            return (
              <div className="card mb-6 bg-blue-50 border-blue-200">
                <h3 className="text-lg font-semibold mb-4">📊 Tüm Sonuçlar (En İyiden En Kötüye)</h3>
                <div className="space-y-3">
                  {sortedTools.map((tool, index) => {
                    const metrics = results?.metrics?.[tool]
                    if (!metrics) return null

                    // Ortalama doğruluk hesapla
                    const avgScore = computeCompositeScore(metrics)
                    const accuracy = (avgScore * 100).toFixed(1)

                    return (
                      <div key={tool} className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm">
                        <div className="flex items-center gap-3">
                          <div className="text-3xl">{medals[index] || '🏅'}</div>
                          <div>
                            <div className={`text-lg font-bold ${colors[index] || 'text-gray-700'}`}>
                              {toolNames[tool]}
                            </div>
                            <div className="text-sm text-gray-500">
                              Sıra: {index + 1}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-3xl font-bold ${colors[index] || 'text-gray-700'}`}>
                            {accuracy}%
                          </div>
                          <div className="text-xs text-gray-500">Doğruluk</div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })()}

          {/* Detaylı Çeviri Kartları */}
          {(() => {
            // Araçları doğruluk oranına göre sırala
            const sortedTools = results.metrics && Object.keys(results.metrics).length > 0
              ? [...selectedTools].sort((a, b) => {
                const scoreA = results.metrics[a] ? computeCompositeScore(results.metrics[a]) : -1
                const scoreB = results.metrics[b] ? computeCompositeScore(results.metrics[b]) : -1

                return scoreB - scoreA
              })
              : selectedTools

            return (
              <div>
                <h3 className="text-xl font-semibold mb-4">Detaylı Çeviri Sonuçları</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {sortedTools.map(tool => (
                    <TranslationCard
                      key={tool}
                      tool={tool}
                      translation={results?.translations?.[tool]}
                      metrics={results?.metrics?.[tool]}
                      timeTaken={results?.time_taken_ms?.[tool]}
                      isLoading={isLoading}
                    />
                  ))}
                </div>
              </div>
            )
          })()}
        </div>
      )}
    </div>
  )
}

export default Compare
