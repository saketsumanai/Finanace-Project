import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, TrendingUp, DollarSign, BarChart3, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { projectService } from '@/services/projectService'
import { uploadService } from '@/services/uploadService'
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
  Filler,
  ArcElement
} from 'chart.js'
import { Line, Bar, Pie } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default function AnalyticsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: project, isLoading: loadingProject } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectService.getProject(id!),
    enabled: !!id,
  })

  const { data: filesList, isLoading: loadingFiles } = useQuery({
    queryKey: ['files', id],
    queryFn: () => uploadService.listProjectFiles(Number(id!)),
    enabled: !!id,
  })

  if (loadingProject || loadingFiles) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    )
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-text-secondary-light dark:text-text-secondary-dark">
          Project not found
        </div>
      </div>
    )
  }

  const productionFiles = filesList?.files.filter(f => f.file_type === 'production') || []
  const financialFiles = filesList?.files.filter(f => f.file_type === 'financial') || []

  // Sample data for demonstration
  const sampleProductionData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Oil Production (bbl)',
        data: [1000, 950, 900, 855, 812, 771, 732, 695, 660, 627, 596, 566],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Gas Production (MCF)',
        data: [5000, 4750, 4500, 4275, 4061, 3858, 3665, 3481, 3305, 3140, 2983, 2834],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  const sampleRevenueData = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'Revenue',
        data: [2500000, 2350000, 2200000, 2100000],
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
      },
      {
        label: 'OPEX',
        data: [800000, 820000, 840000, 860000],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
      },
      {
        label: 'CAPEX',
        data: [500000, 300000, 200000, 100000],
        backgroundColor: 'rgba(249, 115, 22, 0.8)',
      },
    ],
  }

  const sampleFileTypeData = {
    labels: ['Production Files', 'Financial Files'],
    datasets: [
      {
        data: [productionFiles.length, financialFiles.length],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(34, 197, 94, 0.8)',
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(34, 197, 94)',
        ],
        borderWidth: 1,
      },
    ],
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate(`/projects/${id}`)}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
          <div>
            <h1 className="text-3xl font-bold">Analytics & Visualizations</h1>
            <p className="text-gray-600 mt-1">{project.name}</p>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Files</p>
              <p className="text-2xl font-bold">{filesList?.files.length || 0}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Production Files</p>
              <p className="text-2xl font-bold">{productionFiles.length}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Financial Files</p>
              <p className="text-2xl font-bold">{financialFiles.length}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <DollarSign className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Scenarios</p>
              <p className="text-2xl font-bold">{project.scenarios_count || 0}</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Production Trend Chart */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold mb-4">Production Trends</h3>
            <div className="h-80">
              <Line
                data={sampleProductionData}
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
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'Volume',
                      },
                    },
                  },
                }}
              />
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Sample data showing production decline over 12 months
            </p>
          </div>
        </Card>

        {/* Revenue & Costs Chart */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold mb-4">Revenue & Costs</h3>
            <div className="h-80">
              <Bar
                data={sampleRevenueData}
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
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'Amount ($)',
                      },
                      ticks: {
                        callback: function(value) {
                          return '$' + (value as number / 1000000).toFixed(1) + 'M'
                        }
                      }
                    },
                  },
                }}
              />
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Sample quarterly revenue and cost breakdown
            </p>
          </div>
        </Card>

        {/* File Distribution Chart */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold mb-4">Data Files Distribution</h3>
            <div className="h-80 flex items-center justify-center">
              <div className="w-64">
                <Pie
                  data={sampleFileTypeData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Distribution of uploaded data files by type
            </p>
          </div>
        </Card>

        {/* Data Quality Card */}
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-semibold mb-4">Data Quality Overview</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Production Data Completeness</span>
                  <span className="font-medium">
                    {productionFiles.length > 0 ? '100%' : '0%'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: productionFiles.length > 0 ? '100%' : '0%' }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Financial Data Completeness</span>
                  <span className="font-medium">
                    {financialFiles.length > 0 ? '100%' : '0%'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: financialFiles.length > 0 ? '100%' : '0%' }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Modeling Readiness</span>
                  <span className="font-medium">
                    {productionFiles.length > 0 && financialFiles.length > 0 ? '100%' : '50%'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-purple-500 h-2 rounded-full"
                    style={{ 
                      width: productionFiles.length > 0 && financialFiles.length > 0 ? '100%' : '50%' 
                    }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-sm text-blue-900 dark:text-blue-300">
                {productionFiles.length === 0 && financialFiles.length === 0 ? (
                  <>
                    <strong>No data uploaded yet.</strong> Upload production and financial data to see real analytics.
                  </>
                ) : productionFiles.length === 0 ? (
                  <>
                    <strong>Upload production data</strong> to complete your dataset and run valuations.
                  </>
                ) : financialFiles.length === 0 ? (
                  <>
                    <strong>Upload financial data</strong> to complete your dataset and run valuations.
                  </>
                ) : (
                  <>
                    <strong>Data complete!</strong> You can now run financial modeling and valuations.
                  </>
                )}
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Action Buttons */}
      <Card>
        <div className="p-6">
          <h3 className="text-lg font-semibold mb-4">Next Steps</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              onClick={() => navigate(`/projects/${id}`)}
              variant="secondary"
              className="w-full"
            >
              Upload More Data
            </Button>
            <Button
              onClick={() => navigate(`/projects/${id}/modeling`)}
              className="w-full"
            >
              Financial Modeling
            </Button>
            <Button
              onClick={() => window.location.reload()}
              variant="secondary"
              className="w-full"
            >
              Refresh Analytics
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
