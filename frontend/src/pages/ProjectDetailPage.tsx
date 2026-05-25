import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Calculator, Upload, TrendingUp, BarChart2 } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { projectService } from '@/services/projectService'
import { uploadService } from '@/services/uploadService'
import FileUploadModal from '@/components/upload/FileUploadModal'

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [showUploadModal, setShowUploadModal] = useState(false)

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => projectService.getProject(id!),
    enabled: !!id,
  })

  const { data: filesList } = useQuery({
    queryKey: ['files', id],
    queryFn: () => uploadService.listProjectFiles(Number(id!)),
    enabled: !!id,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-text-secondary-light dark:text-text-secondary-dark">
          Loading project...
        </div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-text-secondary-light dark:text-text-secondary-dark">
          Project not found
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark">
            {project.name}
          </h1>
          {project.description && (
            <p className="text-text-secondary-light dark:text-text-secondary-dark mt-2">
              {project.description}
            </p>
          )}
        </div>
        <Button onClick={() => navigate(`/projects/${id}/modeling`)}>
          <Calculator className="w-4 h-4 mr-2" />
          Financial Modeling
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Status">
          <div className="text-2xl font-bold text-text-primary-light dark:text-text-primary-dark capitalize">
            {project.status}
          </div>
        </Card>

        <Card title="Files Uploaded">
          <div className="text-2xl font-bold text-text-primary-light dark:text-text-primary-dark">
            {filesList?.files.length || 0}
          </div>
        </Card>

        <Card title="Scenarios">
          <div className="text-2xl font-bold text-text-primary-light dark:text-text-primary-dark">
            {project.scenarios_count}
          </div>
        </Card>
      </div>

      <Card title="Project Details">
        <div className="space-y-4">
          <div>
            <div className="text-sm text-text-secondary-light dark:text-text-secondary-dark">
              Created
            </div>
            <div className="text-text-primary-light dark:text-text-primary-dark">
              {new Date(project.created_at).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-sm text-text-secondary-light dark:text-text-secondary-dark">
              Last Updated
            </div>
            <div className="text-text-primary-light dark:text-text-primary-dark">
              {new Date(project.updated_at).toLocaleString()}
            </div>
          </div>
        </div>
      </Card>

      {/* Quick Actions */}
      <Card title="Quick Actions">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => navigate(`/projects/${id}/modeling`)}
            className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors text-center"
          >
            <Calculator className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Financial Modeling</h3>
            <p className="text-sm text-gray-600">Create assumptions and run valuations</p>
          </button>
          
          <button
            onClick={() => setShowUploadModal(true)}
            className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors text-center"
          >
            <Upload className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Upload Data</h3>
            <p className="text-sm text-gray-600">Upload production and financial data</p>
          </button>
          
          <button
            onClick={() => navigate(`/projects/${id}/analytics`)}
            className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors text-center"
          >
            <BarChart2 className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Analytics</h3>
            <p className="text-sm text-gray-600">View charts and data visualizations</p>
          </button>
        </div>
      </Card>

      {/* Uploaded Files List */}
      {filesList && filesList.files.length > 0 && (
        <Card title="Uploaded Files">
          <div className="space-y-3">
            {filesList.files.map((file) => (
              <div
                key={file.file_id}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <Upload className="w-5 h-5 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900 dark:text-white">
                      {file.filename}
                    </div>
                    <div className="text-sm text-gray-500">
                      {file.file_type} • {(file.file_size / 1024).toFixed(2)} KB • {file.status}
                    </div>
                  </div>
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(file.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <FileUploadModal
          projectId={Number(id)}
          onClose={() => setShowUploadModal(false)}
        />
      )}
    </div>
  )
}
