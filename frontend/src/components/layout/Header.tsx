import { Moon, Sun, LogOut } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useThemeStore } from '@/store/themeStore'
import { useAuthStore } from '@/store/authStore'
import { Button } from '@/components/ui/Button'

export default function Header() {
  const navigate = useNavigate()
  const { mode, toggleTheme } = useThemeStore()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark h-16 fixed top-0 left-0 right-0 z-50">
      <div className="h-full px-6 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-text-primary-light dark:text-text-primary-dark">
            Oil & Gas M&A Valuation
          </h1>
        </div>

        <div className="flex items-center space-x-4">
          <span className="text-sm text-text-secondary-light dark:text-text-secondary-dark">
            {user?.full_name}
          </span>
          
          <button
            onClick={toggleTheme}
            className="p-2 rounded-md hover:bg-background-light dark:hover:bg-background-dark transition-colors"
            aria-label="Toggle theme"
          >
            {mode === 'light' ? (
              <Moon className="h-5 w-5 text-text-primary-light dark:text-text-primary-dark" />
            ) : (
              <Sun className="h-5 w-5 text-text-primary-light dark:text-text-primary-dark" />
            )}
          </button>

          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>
      </div>
    </header>
  )
}
