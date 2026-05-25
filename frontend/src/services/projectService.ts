import api from './api'

export interface Project {
  id: string
  owner_id: string
  name: string
  description: string | null
  project_type: string
  status: 'draft' | 'active' | 'archived'
  created_at: string
  updated_at: string
}

export interface ProjectDetail extends Project {
  files_count: number
  scenarios_count: number
}

export interface ProjectList {
  items: Project[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface CreateProjectData {
  name: string
  description?: string
  project_type: string
}

export interface UpdateProjectData {
  name?: string
  description?: string
  status?: 'draft' | 'active' | 'archived'
}

export interface ProjectFilters {
  page?: number
  page_size?: number
  status?: 'draft' | 'active' | 'archived'
  sort_by?: 'created_at' | 'updated_at' | 'name'
  sort_order?: 'asc' | 'desc'
}

export const projectService = {
  async getProjects(filters?: ProjectFilters): Promise<ProjectList> {
    const response = await api.get<ProjectList>('/projects', { params: filters })
    return response.data
  },

  async getProject(id: string): Promise<ProjectDetail> {
    const response = await api.get<ProjectDetail>(`/projects/${id}`)
    return response.data
  },

  async createProject(data: CreateProjectData): Promise<Project> {
    const response = await api.post<Project>('/projects', data)
    return response.data
  },

  async updateProject(id: string, data: UpdateProjectData): Promise<Project> {
    const response = await api.put<Project>(`/projects/${id}`, data)
    return response.data
  },

  async deleteProject(id: string): Promise<void> {
    await api.delete(`/projects/${id}`)
  },
}
