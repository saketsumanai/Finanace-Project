import { TrendingUp, DollarSign, Clock, Target, BarChart3, PieChart } from 'lucide-react'
import { Card } from '../ui/Card'
import { ValuationMetrics, AnnualData } from '@/services/modelingService'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

interface ValuationResultsProps {
  metrics: ValuationMetrics
  annualData?: AnnualData[]
  scenarioName: string
  scenarioType: string
}

export default function ValuationResults({ metrics, annualData, scenarioName, scenarioType }: ValuationResultsProps) {
  const formatCurrency = (value?: number) => {
    if (value === undefined || value === null) return 'N/A'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const formatPercentage = (value?: number) => {
    if (value === undefined || value === null) return 'N/A'
    return `${(value * 100).toFixed(2)}%`
  }

  const formatNumber = (value?: number, decimals: number = 1) => {
    if (value === undefined || value === null) return 'N/A'
    return value.toFixed(decimals)
  }

  const getScenarioColor = (type: string) => {
    switch (type) {
      case 'bull':
        return 'bg-green-100 text-green-800'
      case 'bear':
        return 'bg-red-100 text-red-800'
      case 'base':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">{scenarioName}</h2>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium mt-2 ${getScenarioColor(scenarioType)}`}>
            {scenarioType.charAt(0).toUpperCase() + scenarioType.slice(1)} Case
          </span>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* NPV */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Net Present Value</p>
              <p className="text-2xl font-bold">{formatCurrency(metrics.npv)}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <DollarSign className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Discounted cash flow value
          </div>
        </Card>

        {/* IRR */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Internal Rate of Return</p>
              <p className="text-2xl font-bold">{formatPercentage(metrics.irr)}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Annual return rate
          </div>
        </Card>

        {/* Payback Period */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Payback Period</p>
              <p className="text-2xl font-bold">{formatNumber(metrics.payback_period)} years</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Clock className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Time to recover investment
          </div>
        </Card>

        {/* ROIC */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Return on Invested Capital</p>
              <p className="text-2xl font-bold">{formatPercentage(metrics.roic)}</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Target className="w-6 h-6 text-orange-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Capital efficiency
          </div>
        </Card>

        {/* ROI */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Return on Investment</p>
              <p className="text-2xl font-bold">{formatPercentage(metrics.roi)}</p>
            </div>
            <div className="p-3 bg-indigo-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-indigo-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Total return percentage
          </div>
        </Card>

        {/* Profitability Index */}
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Profitability Index</p>
              <p className="text-2xl font-bold">{formatNumber(metrics.profitability_index, 2)}</p>
            </div>
            <div className="p-3 bg-pink-100 rounded-lg">
              <PieChart className="w-6 h-6 text-pink-600" />
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-500">
            Value per dollar invested
          </div>
        </Card>
      </div>

      {/* Terminal Value */}
      {metrics.terminal_value && (
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Terminal Value</p>
              <p className="text-3xl font-bold">{formatCurrency(metrics.terminal_value)}</p>
            </div>
            <div className="text-sm text-gray-500">
              Exit value at end of forecast period
            </div>
          </div>
        </Card>
      )}

      {/* Charts Section */}
      {annualData && annualData.length > 0 && (
        <>
          {/* Production Decline Chart */}
          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold mb-4">Production Forecast</h3>
              <div className="h-80">
                <Line
                  data={{
                    labels: annualData.map(d => `Year ${d.year}`),
                    datasets: [
                      {
                        label: 'Oil Production (bbl)',
                        data: annualData.map(d => d.oil_production),
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y',
                      },
                      {
                        label: 'Gas Production (MCF)',
                        data: annualData.map(d => d.gas_production),
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y1',
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                      mode: 'index',
                      intersect: false,
                    },
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: false,
                      },
                    },
                    scales: {
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                          display: true,
                          text: 'Oil (bbl)',
                        },
                      },
                      y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Gas (MCF)',
                        },
                        grid: {
                          drawOnChartArea: false,
                        },
                      },
                    },
                  }}
                />
              </div>
            </div>
          </Card>

          {/* Cash Flow Chart */}
          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold mb-4">Cash Flow Analysis</h3>
              <div className="h-80">
                <Bar
                  data={{
                    labels: annualData.slice(0, 10).map(d => `Year ${d.year}`),
                    datasets: [
                      {
                        label: 'Revenue',
                        data: annualData.slice(0, 10).map(d => d.revenue),
                        backgroundColor: 'rgba(34, 197, 94, 0.8)',
                      },
                      {
                        label: 'OPEX',
                        data: annualData.slice(0, 10).map(d => -d.opex),
                        backgroundColor: 'rgba(239, 68, 68, 0.8)',
                      },
                      {
                        label: 'CAPEX',
                        data: annualData.slice(0, 10).map(d => -d.capex),
                        backgroundColor: 'rgba(249, 115, 22, 0.8)',
                      },
                      {
                        label: 'Free Cash Flow',
                        data: annualData.slice(0, 10).map(d => d.free_cash_flow),
                        backgroundColor: 'rgba(59, 130, 246, 0.8)',
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: false,
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                              label += ': ';
                            }
                            if (context.parsed.y !== null) {
                              label += new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD',
                                minimumFractionDigits: 0,
                              }).format(Math.abs(context.parsed.y));
                            }
                            return label;
                          }
                        }
                      }
                    },
                    scales: {
                      y: {
                        title: {
                          display: true,
                          text: 'Amount ($)',
                        },
                        ticks: {
                          callback: function(value) {
                            return new Intl.NumberFormat('en-US', {
                              style: 'currency',
                              currency: 'USD',
                              minimumFractionDigits: 0,
                              notation: 'compact',
                            }).format(value as number);
                          }
                        }
                      },
                    },
                  }}
                />
              </div>
            </div>
          </Card>

          {/* EBITDA and Synergies Chart */}
          <Card>
            <div className="p-6">
              <h3 className="text-lg font-semibold mb-4">EBITDA & Synergies</h3>
              <div className="h-80">
                <Line
                  data={{
                    labels: annualData.slice(0, 10).map(d => `Year ${d.year}`),
                    datasets: [
                      {
                        label: 'EBITDA',
                        data: annualData.slice(0, 10).map(d => d.ebitda),
                        borderColor: 'rgb(99, 102, 241)',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.4,
                      },
                      {
                        label: 'Synergy Value',
                        data: annualData.slice(0, 10).map(d => d.synergy_value),
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        fill: true,
                        tension: 0.4,
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: false,
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                              label += ': ';
                            }
                            if (context.parsed.y !== null) {
                              label += new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD',
                                minimumFractionDigits: 0,
                              }).format(context.parsed.y);
                            }
                            return label;
                          }
                        }
                      }
                    },
                    scales: {
                      y: {
                        title: {
                          display: true,
                          text: 'Amount ($)',
                        },
                        ticks: {
                          callback: function(value) {
                            return new Intl.NumberFormat('en-US', {
                              style: 'currency',
                              currency: 'USD',
                              minimumFractionDigits: 0,
                              notation: 'compact',
                            }).format(value as number);
                          }
                        }
                      },
                    },
                  }}
                />
              </div>
            </div>
          </Card>
        </>
      )}

      {/* Annual Data Table */}
      {annualData && annualData.length > 0 && (
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold mb-4">Annual Forecast Data</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Year</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">Oil (bbl)</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">Gas (MCF)</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">Revenue</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">OPEX</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">CAPEX</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">EBITDA</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">Synergies</th>
                    <th className="px-4 py-3 text-right font-medium text-gray-700">FCF</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {annualData.slice(0, 10).map((data) => (
                    <tr key={data.year} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium">{data.year}</td>
                      <td className="px-4 py-3 text-right">{formatNumber(data.oil_production, 0)}</td>
                      <td className="px-4 py-3 text-right">{formatNumber(data.gas_production, 0)}</td>
                      <td className="px-4 py-3 text-right">{formatCurrency(data.revenue)}</td>
                      <td className="px-4 py-3 text-right">{formatCurrency(data.opex)}</td>
                      <td className="px-4 py-3 text-right">{formatCurrency(data.capex)}</td>
                      <td className="px-4 py-3 text-right font-medium">{formatCurrency(data.ebitda)}</td>
                      <td className="px-4 py-3 text-right text-green-600">{formatCurrency(data.synergy_value)}</td>
                      <td className="px-4 py-3 text-right font-medium">{formatCurrency(data.free_cash_flow)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {annualData.length > 10 && (
              <div className="mt-4 text-center text-sm text-gray-500">
                Showing first 10 of {annualData.length} years
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Investment Decision */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Investment Decision Indicators</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="font-medium">NPV Positive?</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              (metrics.npv ?? 0) > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {(metrics.npv ?? 0) > 0 ? 'Yes ✓' : 'No ✗'}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="font-medium">IRR {'>'} 12% (typical hurdle)?</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              (metrics.irr ?? 0) > 0.12 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {(metrics.irr ?? 0) > 0.12 ? 'Yes ✓' : 'No ✗'}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="font-medium">Profitability Index {'>'} 1.0?</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              (metrics.profitability_index ?? 0) > 1.0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {(metrics.profitability_index ?? 0) > 1.0 ? 'Yes ✓' : 'No ✗'}
            </span>
          </div>
        </div>
      </Card>
    </div>
  )
}
