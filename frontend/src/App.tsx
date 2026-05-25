import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import AuthCallbackPage from './pages/AuthCallbackPage'
import DashboardLayout from './components/layout/DashboardLayout'
import ProjectsPage from './pages/ProjectsPage'
import ProjectDetailPage from './pages/ProjectDetailPage'
import ModelingPage from './pages/ModelingPage'
import AnalyticsPage from './pages/AnalyticsPage'
import AIChatPage from './pages/AIChatPage'

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/projects" /> : <LoginPage />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/projects" /> : <RegisterPage />}
        />
        <Route path="/auth/callback" element={<AuthCallbackPage />} />

        {/* Protected routes */}
        <Route
          path="/"
          element={isAuthenticated ? <DashboardLayout /> : <Navigate to="/login" />}
        >
          <Route index element={<Navigate to="/projects" />} />
          <Route path="projects" element={<ProjectsPage />} />
          <Route path="projects/:id" element={<ProjectDetailPage />} />
          <Route path="projects/:projectId/modeling" element={<ModelingPage />} />
          <Route path="projects/:id/analytics" element={<AnalyticsPage />} />
          <Route path="ai-chat" element={<AIChatPage />} />
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
