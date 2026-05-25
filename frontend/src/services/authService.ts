import api from './api'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
}

export interface User {
  id: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', credentials)
    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  },

  async getGoogleAuthUrl(): Promise<{ auth_url: string }> {
    const response = await api.get<{ auth_url: string }>('/auth/google/login')
    return response.data
  },
}
