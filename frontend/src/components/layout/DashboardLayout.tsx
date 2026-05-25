import { Outlet } from 'react-router-dom'
import Header from './Header.tsx'
import Sidebar from './Sidebar.tsx'

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 ml-64">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
