import { NavLink } from 'react-router-dom'
import { FolderOpen, BarChart3, Settings, Sparkles } from 'lucide-react'
import { cn } from '@/utils/cn'

const navigation = [
  { name: 'Projects', href: '/projects', icon: FolderOpen },
  { name: 'AI Chat', href: '/ai-chat', icon: Sparkles, highlight: true },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-surface-light dark:bg-surface-dark border-r border-border-light dark:border-border-dark fixed left-0 top-16 bottom-0 overflow-y-auto">
      <nav className="p-4 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              cn(
                'flex items-center space-x-3 px-4 py-3 rounded-md transition-colors',
                item.highlight && !isActive
                  ? 'bg-gradient-to-r from-purple-600/10 to-blue-600/10 text-purple-600 dark:text-purple-400 hover:from-purple-600/20 hover:to-blue-600/20'
                  : isActive
                  ? item.highlight
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                    : 'bg-primary text-white'
                  : 'text-text-primary-light dark:text-text-primary-dark hover:bg-background-light dark:hover:bg-background-dark'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            <span className="font-medium">{item.name}</span>
            {item.highlight && (
              <span className="ml-auto text-xs bg-gradient-to-r from-purple-600 to-blue-600 text-white px-2 py-0.5 rounded-full">
                AI
              </span>
            )}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
