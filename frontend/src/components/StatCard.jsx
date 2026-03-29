function StatCard({ title, value, icon, trend }) {
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p className="text-sm text-gray-500 mt-1">{trend}</p>
          )}
        </div>
        {icon && (
          <div className="text-4xl text-primary-500">
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}

export default StatCard
