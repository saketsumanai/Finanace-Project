import api from './api'

// ==================== TYPES ====================

export interface PriceForecast {
  year: number
  price: number
}

export interface CapexScheduleItem {
  year: number
  amount: number
}

export interface SynergyRealizationItem {
  year: number
  percentage: number
}

export interface Assumptions {
  id: string
  project_id: string
  version: number
  name: string
  
  // Production assumptions
  decline_curve_type: 'exponential' | 'hyperbolic' | 'harmonic'
  decline_rate: number
  hyperbolic_b?: number
  oil_price_forecast?: PriceForecast[]
  gas_price_forecast?: PriceForecast[]
  
  // Cost assumptions
  opex_inflation_rate?: number
  capex_schedule?: CapexScheduleItem[]
  transportation_cost_per_unit?: number
  ga_annual?: number
  
  // Deal assumptions
  purchase_price?: number
  debt_amount?: number
  equity_amount?: number
  discount_rate?: number
  tax_rate?: number
  exit_multiple?: number
  forecast_years?: number
  
  created_at: string
  updated_at: string
}

export interface CreateAssumptionsData {
  project_id: string
  name: string
  version?: number
  
  // Production assumptions
  decline_curve_type: 'exponential' | 'hyperbolic' | 'harmonic'
  decline_rate: number
  hyperbolic_b?: number
  oil_price_forecast?: PriceForecast[]
  gas_price_forecast?: PriceForecast[]
  
  // Cost assumptions
  opex_inflation_rate?: number
  capex_schedule?: CapexScheduleItem[]
  transportation_cost_per_unit?: number
  ga_annual?: number
  
  // Deal assumptions
  purchase_price: number
  debt_amount?: number
  equity_amount?: number
  discount_rate?: number
  tax_rate?: number
  exit_multiple?: number
  forecast_years?: number
}

export interface SynergyModel {
  id: string
  assumptions_id: string
  category: 'operational_overhead' | 'procurement_efficiency' | 'workforce_consolidation' | 'shared_infrastructure'
  description?: string
  target_value: number
  realization_schedule: SynergyRealizationItem[]
  created_at: string
}

export interface CreateSynergyModelData {
  category: 'operational_overhead' | 'procurement_efficiency' | 'workforce_consolidation' | 'shared_infrastructure'
  description?: string
  target_value: number
  realization_schedule: SynergyRealizationItem[]
}

export interface Scenario {
  id: string
  project_id: string
  assumptions_id: string
  name: string
  scenario_type: 'bull' | 'base' | 'bear' | 'custom'
  description?: string
  created_at: string
}

export interface CreateScenarioData {
  project_id: string
  assumptions_id: string
  name: string
  scenario_type: 'bull' | 'base' | 'bear' | 'custom'
  description?: string
}

export interface ValuationMetrics {
  npv?: number
  irr?: number
  payback_period?: number
  roi?: number
  roic?: number
  profitability_index?: number
  terminal_value?: number
}

export interface AnnualData {
  year: number
  oil_production: number
  gas_production: number
  revenue: number
  opex: number
  capex: number
  ebitda: number
  synergy_value: number
  free_cash_flow: number
  taxes: number
}

export interface ValuationSummary {
  scenario_id: string
  scenario_name: string
  scenario_type: string
  metrics: ValuationMetrics
  summary_financials?: {
    total_revenue: number
    total_opex: number
    total_capex: number
    total_synergies: number
    total_ebitda: number
    total_fcf: number
    avg_annual_ebitda: number
    year_1_ebitda: number
    final_year_ebitda: number
  }
  production_summary?: {
    initial_oil_rate: number
    initial_gas_rate: number
    total_oil_production: number
    total_gas_production: number
    decline_curve_type: string
    decline_rate: number
  }
}

export interface ValuationResults {
  scenario_id: string
  scenario_name: string
  scenario_type: string
  metrics: ValuationMetrics
  annual_data: AnnualData[]
}

export interface ScenarioComparison {
  scenario_id: string
  scenario_name: string
  scenario_type: string
  npv?: number
  irr?: number
  payback_period?: number
  roic?: number
}

// ==================== API FUNCTIONS ====================

export const modelingService = {
  // ==================== ASSUMPTIONS ====================
  
  async getAssumptions(assumptionsId: string): Promise<Assumptions> {
    const response = await api.get<Assumptions>(`/modeling/assumptions/${assumptionsId}`)
    return response.data
  },

  async listProjectAssumptions(projectId: string): Promise<Assumptions[]> {
    const response = await api.get<Assumptions[]>(`/modeling/projects/${projectId}/assumptions`)
    return response.data
  },

  async createAssumptions(data: CreateAssumptionsData): Promise<Assumptions> {
    const response = await api.post<Assumptions>('/modeling/assumptions', data)
    return response.data
  },

  async updateAssumptions(assumptionsId: string, data: Partial<CreateAssumptionsData>): Promise<Assumptions> {
    const response = await api.put<Assumptions>(`/modeling/assumptions/${assumptionsId}`, data)
    return response.data
  },

  async deleteAssumptions(assumptionsId: string): Promise<void> {
    await api.delete(`/modeling/assumptions/${assumptionsId}`)
  },

  // ==================== SYNERGY MODELS ====================
  
  async listSynergyModels(assumptionsId: string): Promise<SynergyModel[]> {
    const response = await api.get<SynergyModel[]>(`/modeling/assumptions/${assumptionsId}/synergies`)
    return response.data
  },

  async createSynergyModel(assumptionsId: string, data: CreateSynergyModelData): Promise<SynergyModel> {
    const response = await api.post<SynergyModel>(`/modeling/assumptions/${assumptionsId}/synergies`, data)
    return response.data
  },

  async deleteSynergyModel(synergyId: string): Promise<void> {
    await api.delete(`/modeling/synergies/${synergyId}`)
  },

  // ==================== SCENARIOS ====================
  
  async getScenario(scenarioId: string): Promise<Scenario> {
    const response = await api.get<Scenario>(`/modeling/scenarios/${scenarioId}`)
    return response.data
  },

  async listProjectScenarios(projectId: string): Promise<Scenario[]> {
    const response = await api.get<Scenario[]>(`/modeling/projects/${projectId}/scenarios`)
    return response.data
  },

  async createScenario(data: CreateScenarioData): Promise<Scenario> {
    const response = await api.post<Scenario>('/modeling/scenarios', data)
    return response.data
  },

  async updateScenario(scenarioId: string, data: Partial<CreateScenarioData>): Promise<Scenario> {
    const response = await api.put<Scenario>(`/modeling/scenarios/${scenarioId}`, data)
    return response.data
  },

  async deleteScenario(scenarioId: string): Promise<void> {
    await api.delete(`/modeling/scenarios/${scenarioId}`)
  },

  // ==================== VALUATION ====================
  
  async runValuation(scenarioId: string, periodsPerYear: number = 12): Promise<ValuationSummary> {
    const response = await api.post<ValuationSummary>('/modeling/valuation/run', {
      scenario_id: scenarioId,
      periods_per_year: periodsPerYear,
    })
    return response.data
  },

  async getValuationResults(scenarioId: string): Promise<ValuationResults> {
    const response = await api.get<ValuationResults>(`/modeling/valuation/results/${scenarioId}`)
    return response.data
  },

  async compareScenarios(scenarioIds: string[]): Promise<{ scenarios: ScenarioComparison[] }> {
    const response = await api.post<{ scenarios: ScenarioComparison[] }>('/modeling/valuation/compare', {
      scenario_ids: scenarioIds,
    })
    return response.data
  },
}
