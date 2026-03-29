import { Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

function RadarChart({ data, title }) {
  const metrics = ['BLEU', 'METEOR', 'chrF++', 'TER (inv)']
  const tools = Object.keys(data)
  
  const datasets = tools.map((tool, index) => {
    const colors = [
      'rgba(59, 130, 246, 0.6)',
      'rgba(99, 102, 241, 0.6)',
      'rgba(6, 182, 212, 0.6)',
      'rgba(249, 115, 22, 0.6)'
    ]
    
    const borderColors = [
      'rgb(59, 130, 246)',
      'rgb(99, 102, 241)',
      'rgb(6, 182, 212)',
      'rgb(249, 115, 22)'
    ]
    
    return {
      label: tool,
      data: [
        data[tool].bleu || 0,
        data[tool].meteor || 0,
        data[tool].chrf || 0,
        1 - (data[tool].ter || 0)
      ],
      backgroundColor: colors[index % colors.length],
      borderColor: borderColors[index % borderColors.length],
      borderWidth: 2
    }
  })
  
  const chartData = {
    labels: metrics,
    datasets
  }
  
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: title,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 1,
        ticks: {
          stepSize: 0.2
        }
      }
    }
  }
  
  return (
    <div className="h-96">
      <Radar data={chartData} options={options} />
    </div>
  )
}

export default RadarChart
