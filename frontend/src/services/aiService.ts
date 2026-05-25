/**
 * AI Service for Gemini-powered features
 */
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/ai';

export interface ChatMessage {
  message: string;
  project_id?: number;
}

export interface ChatResponse {
  response: string;
  suggestions?: string[];
}

export interface ProjectAnalysis {
  success: boolean;
  project_id: number;
  analysis: {
    risks?: string[];
    assumptions?: any;
    synergies?: string[];
    deal_structure?: string;
    due_diligence?: string[];
    analysis?: string;
  };
}

export interface OptimizedAssumptions {
  success: boolean;
  project_id: number;
  recommendations: {
    decline_curve_type: string;
    decline_rate: number;
    discount_rate: number;
    forecast_years: number;
    exit_multiple: number;
    reasoning?: string;
  };
}

export interface ResultsAnalysis {
  success: boolean;
  scenario_id: number;
  analysis: {
    recommendation: string;
    rating: number;
    strengths?: string[];
    concerns?: string[];
    sensitivities?: string[];
    price_range?: string;
    analysis?: string;
  };
}

export interface SynergySuggestion {
  category: string;
  description: string;
  target_value: number;
  years: number;
  confidence: string;
}

export interface SynergySuggestions {
  success: boolean;
  project_id: number;
  synergies: SynergySuggestion[];
}

export interface ExecutiveReport {
  success: boolean;
  scenario_id: number;
  executive_summary: string;
}

export interface CSVAnalysis {
  success: boolean;
  filename: string;
  statistics?: {
    rows: number;
    columns: number;
    column_names: string[];
    data_types: Record<string, string>;
    missing_values: Record<string, number>;
    sample_data: any[];
  };
  numeric_statistics?: Record<string, any>;
  ai_analysis?: string;
  data_preview?: any[];
  error?: string;
  message?: string;
}

class AIService {
  private getAuthHeader() {
    const token = localStorage.getItem('token');
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }

  async chat(message: string, projectId?: number): Promise<ChatResponse> {
    const response = await axios.post<ChatResponse>(
      `${API_URL}/chat`,
      {
        message,
        project_id: projectId,
      },
      this.getAuthHeader()
    );
    return response.data;
  }

  async analyzeProject(projectId: number): Promise<ProjectAnalysis> {
    const response = await axios.post<ProjectAnalysis>(
      `${API_URL}/analyze-project`,
      { project_id: projectId },
      this.getAuthHeader()
    );
    return response.data;
  }

  async optimizeAssumptions(projectId: number): Promise<OptimizedAssumptions> {
    const response = await axios.post<OptimizedAssumptions>(
      `${API_URL}/optimize-assumptions`,
      { project_id: projectId },
      this.getAuthHeader()
    );
    return response.data;
  }

  async analyzeResults(scenarioId: number): Promise<ResultsAnalysis> {
    const response = await axios.post<ResultsAnalysis>(
      `${API_URL}/analyze-results`,
      { scenario_id: scenarioId },
      this.getAuthHeader()
    );
    return response.data;
  }

  async suggestSynergies(
    projectId: number,
    assumptionsId?: number
  ): Promise<SynergySuggestions> {
    const response = await axios.post<SynergySuggestions>(
      `${API_URL}/suggest-synergies`,
      {
        project_id: projectId,
        assumptions_id: assumptionsId,
      },
      this.getAuthHeader()
    );
    return response.data;
  }

  async generateReport(scenarioId: number): Promise<ExecutiveReport> {
    const response = await axios.post<ExecutiveReport>(
      `${API_URL}/generate-report`,
      { scenario_id: scenarioId },
      this.getAuthHeader()
    );
    return response.data;
  }

  async analyzeCSV(file: File): Promise<CSVAnalysis> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post<CSVAnalysis>(
      `${API_URL}/analyze-csv`,
      formData,
      {
        ...this.getAuthHeader(),
        headers: {
          ...this.getAuthHeader().headers,
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }
}

export const aiService = new AIService();
