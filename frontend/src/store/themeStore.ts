import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ThemeState {
  mode: 'light' | 'dark'
  toggleTheme: () => void
  setTheme: (mode: 'light' | 'dark') => void
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      mode: 'light',
      
      toggleTheme: () => set((state) => {
        const newMode = state.mode === 'light' ? 'dark' : 'light'
        document.documentElement.classList.toggle('dark', newMode === 'dark')
        return { mode: newMode }
      }),
      
      setTheme: (mode) => set(() => {
        document.documentElement.classList.toggle('dark', mode === 'dark')
        return { mode }
      }),
    }),
    {
      name: 'theme-storage',
      onRehydrateStorage: () => (state) => {
        if (state) {
          document.documentElement.classList.toggle('dark', state.mode === 'dark')
        }
      },
    }
  )
)
