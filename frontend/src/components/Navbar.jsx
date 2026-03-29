import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Ana Sayfa' },
    { path: '/compare', label: 'Karşılaştır' },
    { path: '/batch-test', label: 'Toplu Test' },
    { path: '/results', label: 'Sonuçlar' },
    { path: '/datasets', label: 'Dataset' },
    { path: '/analytics', label: 'Analiz' }
  ]
  
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-primary-600">
                MT Karşılaştırma
              </span>
            </Link>
            
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navItems.map(item => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    location.pathname === item.path
                      ? 'border-primary-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
