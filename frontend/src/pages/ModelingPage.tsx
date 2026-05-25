import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { 
  Settings, 
  TrendingUp, 
  Play, 
  Plus, 
  Trash2, 
  Eye,
  ArrowLeft,
  Loader2
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import AssumptionsForm from '@/components/modeling/AssumptionsForm'
import SynergyModelForm from '@/components/modeling/SynergyModelForm'
import ValuationResults from '@/components/modeling/ValuationResults'
import { 
  modelingService, 
  CreateAssumptionsData, 
  CreateSynergyModelData,
  CreateScenarioData,
  Assumptions,
  SynergyModel,
  Scenario
} from '@/services/modelingService'
import { projectService } from '@/services/projectService'

export default function ModelingPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [activeTab, setActiveTab] = useState<'assumptions' | 'synergies' | 'scenarios' | 'results'>('assumptions')
  const [showAssumptionsForm, setShowAssumptionsForm] = useState(false)
  const [showSynergyForm, setShowSynergyForm] = useState(false)
  const [selectedAssumptions, setSelectedAssumptions] = useState<string | null>(null)
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null)
  const [generatingData, setGeneratingData] = useState(false)
  const [showAIInsights, setShowAIInsights] = useState(false)
  const [aiAnalysis, setAIAnalysis] = useState<any>(null)

  // Fetch project
  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectService.getProject(projectId!),
    enabled: !!projectId,
  })

  // Fetch assumptions
  const { data: assumptionsList = [], isLoading: loadingAssumptions } = useQuery({
    queryKey: ['assumptions', projectId],
    queryFn: () => modelingService.listProjectAssumptions(projectId!),
    enabled: !!projectId,
  })

  // Fetch synergy models
  const { data: synergyModels = [] } = useQuery({
    queryKey: ['synergies', selectedAssumptions],
    queryFn: () => modelingService.listSynergyModels(selectedAssumptions!),
    enabled: !!selectedAssumptions,
  })

  // Fetch scenarios
  const { data: scenarios = [] } = useQuery({
    queryKey: ['scenarios', projectId],
    queryFn: () => modelingService.listProjectScenarios(projectId!),
    enabled: !!projectId,
  })

  // Fetch valuation results
  const { data: valuationResults, isLoading: loadingResults } = useQuery({
    queryKey: ['valuation', selectedScenario],
    queryFn: () => modelingService.getValuationResults(selectedScenario!),
    enabled: !!selectedScenario,
  })

  // Create assumptions mutation
  const createAssumptionsMutation = useMutation({
    mutationFn: (data: CreateAssumptionsData) => modelingService.createAssumptions(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['assumptions', projectId] })
      setSelectedAssumptions(data.id)
      setShowAssumptionsForm(false)
      toast.success('Assumptions created successfully')
    },
    onError: () => {
      toast.error('Failed to create assumptions')
    },
  })

  // Create synergy model mutation
  const createSynergyMutation = useMutation({
    mutationFn: (data: CreateSynergyModelData) => 
      modelingService.createSynergyModel(selectedAssumptions!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['synergies', selectedAssumptions] })
      setShowSynergyForm(false)
      toast.success('Synergy model created successfully')
    },
    onError: () => {
      toast.error('Failed to create synergy model')
    },
  })

  // Delete synergy model mutation
  const deleteSynergyMutation = useMutation({
    mutationFn: (synergyId: string) => modelingService.deleteSynergyModel(synergyId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['synergies', selectedAssumptions] })
      toast.success('Synergy model deleted')
    },
    onError: () => {
      toast.error('Failed to delete synergy model')
    },
  })

  // Create scenario mutation
  const createScenarioMutation = useMutation({
    mutationFn: (data: CreateScenarioData) => modelingService.createScenario(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['scenarios', projectId] })
      setSelectedScenario(data.id)
      toast.success('Scenario created successfully')
    },
    onError: () => {
      toast.error('Failed to create scenario')
    },
  })

  // Run valuation mutation
  const runValuationMutation = useMutation({
    mutationFn: (scenarioId: string) => modelingService.runValuation(scenarioId, 12),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['valuation', selectedScenario] })
      setActiveTab('results')
      toast.success('Valuation completed successfully')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to run valuation')
    },
  })

  // Generate smart data mutation
  const generateDataMutation = useMutation({
    mutationFn: async () => {
      const token = localStorage.getItem('token')
      const formData = new FormData()
      formData.append('project_id', projectId!)
      
      const response = await fetch('http://localhost:8000/api/v1/upload/generate-smart-data', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error('Failed to generate data')
      }
      
      return response.json()
    },
    onSuccess: (data) => {
      toast.success(`✨ AI generated ${data.production_records} production records and ${data.financial_records} financial records!`)
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
    },
    onError: () => {
      toast.error('Failed to generate data')
    },
  })

  // Auto-select first assumptions if available
  useEffect(() => {
    if (assumptionsList.length > 0 && !selectedAssumptions) {
      setSelectedAssumptions(assumptionsList[0].id)
    }
  }, [assumptionsList, selectedAssumptions])

  const handleCreateScenario = (type: 'bull' | 'base' | 'bear') => {
    if (!selectedAssumptions) {
      toast.error('Please select assumptions first')
      return
    }

    const scenarioData: CreateScenarioData = {
      project_id: projectId!,
      assumptions_id: selectedAssumptions,
      name: `${type.charAt(0).toUpperCase() + type.slice(1)} Case`,
      scenario_type: type,
      description: `${type.charAt(0).toUpperCase() + type.slice(1)} case scenario`,
    }

    createScenarioMutation.mutate(scenarioData)
  }

  const handleRunValuation = (scenarioId: string) => {
    runValuationMutation.mutate(scenarioId)
  }

  if (!projectId) {
    return <div>Project not found</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate(`/projects/${projectId}`)}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Project
          </Button>
          <div>
            <h1 className="text-3xl font-bold">Financial Modeling</h1>
            <p className="text-gray-600 mt-1">{project?.name}</p>
          </div>
        </div>
        <Button
          onClick={() => generateDataMutation.mutate()}
          disabled={generateDataMutation.isPending}
          className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
        >
          {generateDataMutation.isPending ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              ✨ Generate Smart Data with AI
            </>
          )}
        </Button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {[
            { id: 'assumptions', label: 'Assumptions', icon: Settings },
            { id: 'synergies', label: 'Synergies', icon: TrendingUp },
            { id: 'scenarios', label: 'Scenarios', icon: Play },
            { id: 'results', label: 'Results', icon: Eye },
          ].map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-5 h-5" />
                {tab.label}
              </button>
            )
          })}
        </nav>
      </div>

      {/* AI Data Generation Info Banner */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-2 border-purple-200 dark:border-purple-800 rounded-lg p-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-2xl">✨</span>
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              No Data? No Problem! Use AI to Generate Smart Data
            </h3>
            <p className="text-gray-700 dark:text-gray-300 mb-3">
              Click the <strong>"Generate Smart Data with AI"</strong> button above to automatically create realistic 
              production and financial data based on your project characteristics. The AI analyzes your deal size, 
              project type, and industry standards to generate 12 months of historical data instantly!
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full text-sm font-medium text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-700">
                🎯 Realistic decline curves
              </span>
              <span className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full text-sm font-medium text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700">
                💰 Market-based pricing
              </span>
              <span className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full text-sm font-medium text-green-700 dark:text-green-300 border border-green-200 dark:border-green-700">
                📊 Industry-standard costs
              </span>
              <span className="px-3 py-1 bg-white dark:bg-gray-800 rounded-full text-sm font-medium text-orange-700 dark:text-orange-300 border border-orange-200 dark:border-orange-700">
                ⚡ Instant generation
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div>
        {/* Assumptions Tab */}
        {activeTab === 'assumptions' && (
          <div className="space-y-6">
            {!showAssumptionsForm ? (
              <>
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold">Modeling Assumptions</h2>
                  <Button onClick={() => setShowAssumptionsForm(true)}>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Assumptions
                  </Button>
                </div>

                {loadingAssumptions ? (
                  <div className="flex justify-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                  </div>
                ) : assumptionsList.length === 0 ? (
                  <Card className="p-12 text-center">
                    <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium mb-2">No Assumptions Yet</h3>
                    <p className="text-gray-600 mb-4">
                      Create your first set of modeling assumptions to get started
                    </p>
                    <Button onClick={() => setShowAssumptionsForm(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      Create Assumptions
                    </Button>
                  </Card>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {assumptionsList.map((assumptions) => (
                      <Card
                        key={assumptions.id}
                        className={`p-6 cursor-pointer transition-all ${
                          selectedAssumptions === assumptions.id
                            ? 'ring-2 ring-blue-500 bg-blue-50'
                            : 'hover:shadow-lg'
                        }`}
                        onClick={() => setSelectedAssumptions(assumptions.id)}
                      >
                        <h3 className="font-semibold text-lg mb-2">{assumptions.name}</h3>
                        <div className="space-y-1 text-sm text-gray-600">
                          <p>Version: {assumptions.version}</p>
                          <p>Decline: {assumptions.decline_curve_type}</p>
                          <p>Forecast: {assumptions.forecast_years} years</p>
                          <p className="text-xs text-gray-500 mt-2">
                            Created: {new Date(assumptions.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </Card>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <AssumptionsForm
                projectId={projectId}
                onSubmit={(data) => createAssumptionsMutation.mutate(data)}
                onCancel={() => setShowAssumptionsForm(false)}
              />
            )}
          </div>
        )}

        {/* Synergies Tab */}
        {activeTab === 'synergies' && (
          <div className="space-y-6">
            {!selectedAssumptions ? (
              <Card className="p-12 text-center">
                <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Select Assumptions First</h3>
                <p className="text-gray-600">
                  Please select or create assumptions before adding synergy models
                </p>
              </Card>
            ) : !showSynergyForm ? (
              <>
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold">Synergy Models</h2>
                  <Button onClick={() => setShowSynergyForm(true)}>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Synergy Model
                  </Button>
                </div>

                {synergyModels.length === 0 ? (
                  <Card className="p-12 text-center">
                    <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium mb-2">No Synergy Models</h3>
                    <p className="text-gray-600 mb-4">
                      Add synergy models to capture M&A value creation
                    </p>
                    <Button onClick={() => setShowSynergyForm(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      Add Synergy Model
                    </Button>
                  </Card>
                ) : (
                  <div className="space-y-4">
                    {synergyModels.map((synergy) => (
                      <Card key={synergy.id} className="p-6">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-semibold text-lg mb-2">
                              {synergy.category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </h3>
                            {synergy.description && (
                              <p className="text-gray-600 mb-3">{synergy.description}</p>
                            )}
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              <div>
                                <span className="text-gray-600">Target Value:</span>
                                <span className="ml-2 font-medium">
                                  ${synergy.target_value.toLocaleString()}
                                </span>
                              </div>
                              <div>
                                <span className="text-gray-600">Realization:</span>
                                <span className="ml-2 font-medium">
                                  {synergy.realization_schedule.length} years
                                </span>
                              </div>
                            </div>
                          </div>
                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => deleteSynergyMutation.mutate(synergy.id)}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </Card>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <SynergyModelForm
                onSubmit={(data) => createSynergyMutation.mutate(data)}
                onCancel={() => setShowSynergyForm(false)}
              />
            )}
          </div>
        )}

        {/* Scenarios Tab */}
        {activeTab === 'scenarios' && (
          <div className="space-y-6">
            {!selectedAssumptions ? (
              <Card className="p-12 text-center">
                <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Select Assumptions First</h3>
                <p className="text-gray-600">
                  Please select or create assumptions before creating scenarios
                </p>
              </Card>
            ) : (
              <>
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold">Valuation Scenarios</h2>
                  <div className="flex gap-2">
                    <Button onClick={() => handleCreateScenario('bull')} variant="secondary">
                      <Plus className="w-4 h-4 mr-2" />
                      Bull Case
                    </Button>
                    <Button onClick={() => handleCreateScenario('base')}>
                      <Plus className="w-4 h-4 mr-2" />
                      Base Case
                    </Button>
                    <Button onClick={() => handleCreateScenario('bear')} variant="secondary">
                      <Plus className="w-4 h-4 mr-2" />
                      Bear Case
                    </Button>
                  </div>
                </div>

                {scenarios.length === 0 ? (
                  <Card className="p-12 text-center">
                    <Play className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium mb-2">No Scenarios Yet</h3>
                    <p className="text-gray-600 mb-4">
                      Create Bull/Base/Bear scenarios to run valuations
                    </p>
                  </Card>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {scenarios.map((scenario) => (
                      <Card key={scenario.id} className="p-6">
                        <div className="flex justify-between items-start mb-4">
                          <h3 className="font-semibold text-lg">{scenario.name}</h3>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            scenario.scenario_type === 'bull' ? 'bg-green-100 text-green-800' :
                            scenario.scenario_type === 'bear' ? 'bg-red-100 text-red-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {scenario.scenario_type}
                          </span>
                        </div>
                        {scenario.description && (
                          <p className="text-gray-600 text-sm mb-4">{scenario.description}</p>
                        )}
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            onClick={() => handleRunValuation(scenario.id)}
                            disabled={runValuationMutation.isPending}
                          >
                            {runValuationMutation.isPending ? (
                              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            ) : (
                              <Play className="w-4 h-4 mr-2" />
                            )}
                            Run Valuation
                          </Button>
                          <Button
                            size="sm"
                            variant="secondary"
                            onClick={() => {
                              setSelectedScenario(scenario.id)
                              setActiveTab('results')
                            }}
                          >
                            <Eye className="w-4 h-4 mr-2" />
                            View Results
                          </Button>
                        </div>
                      </Card>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Results Tab */}
        {activeTab === 'results' && (
          <div className="space-y-6">
            {!selectedScenario ? (
              <Card className="p-12 text-center">
                <Eye className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No Scenario Selected</h3>
                <p className="text-gray-600">
                  Please select a scenario and run valuation to see results
                </p>
              </Card>
            ) : loadingResults ? (
              <div className="flex justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
              </div>
            ) : valuationResults ? (
              <ValuationResults
                metrics={valuationResults.metrics}
                annualData={valuationResults.annual_data}
                scenarioName={valuationResults.scenario_name}
                scenarioType={valuationResults.scenario_type}
              />
            ) : (
              <Card className="p-12 text-center">
                <Play className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No Results Available</h3>
                <p className="text-gray-600">
                  Run valuation for this scenario to see results
                </p>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
