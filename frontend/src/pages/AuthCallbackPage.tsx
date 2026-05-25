import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { authService } from '@/services/authService'
import toast from 'react-hot-toast'

export default function AuthCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const setAuth = useAuthStore((state) => state.setAuth)

  useEffect(() => {
    const handleCallback = async () => {
      const token = searchParams.get('token')
      
      if (!token) {
        toast.error('Authentication failed')
        navigate('/login')
        return
      }

      try {
        // Store the token
        localStorage.setItem('token', token)
        
        // Get user info
        const user = await authService.getCurrentUser()
        setAuth(user, token)
        
        toast.success('Successfully signed in with Google!')
        navigate('/projects')
      } catch (error) {
        toast.error('Failed to complete authentication')
        navigate('/login')
      }
    }

    handleCallback()
  }, [searchParams, navigate, setAuth])

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-light dark:bg-surface-dark">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p className="mt-4 text-text-secondary-light dark:text-text-secondary-dark">
          Completing sign in...
        </p>
      </div>
    </div>
  )
}
