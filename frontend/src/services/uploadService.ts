import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface UploadedFile {
  file_id: number
  filename: string
  file_type: string
  file_size: number
  status: string
  quality_score?: number
  created_at: string
}

export interface FileListResponse {
  project_id: number
  files: UploadedFile[]
}

class UploadService {
  private getAuthHeader() {
    const token = localStorage.getItem('token')
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  async uploadFile(
    projectId: number,
    file: File,
    fileType: 'production' | 'financial'
  ): Promise<UploadedFile> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('project_id', projectId.toString())

    const endpoint = fileType === 'production' ? '/production' : '/financials'

    const response = await axios.post(
      `${API_URL}/api/v1/upload${endpoint}`,
      formData,
      {
        headers: {
          ...this.getAuthHeader(),
          'Content-Type': 'multipart/form-data',
        },
      }
    )

    return response.data
  }

  async getFileStatus(fileId: number): Promise<UploadedFile> {
    const response = await axios.get(
      `${API_URL}/api/v1/upload/${fileId}/status`,
      {
        headers: this.getAuthHeader(),
      }
    )

    return response.data
  }

  async listProjectFiles(projectId: number): Promise<FileListResponse> {
    const response = await axios.get(
      `${API_URL}/api/v1/upload/project/${projectId}`,
      {
        headers: this.getAuthHeader(),
      }
    )

    return response.data
  }
}

export const uploadService = new UploadService()
