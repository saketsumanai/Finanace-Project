import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Trash2, Edit, FolderOpen } from 'lucide-react'
import toast from 'react-hot-toast'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { projectService } from '@/services/projectService'
import { useNavigate } from 'react-router-dom'

export default function ProjectsPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [showCreateModal, setShowCreateModal] = useState(false)

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.getProjects(),
  })

  const deleteMutation = useMutation({
    mutationFn: projectService.deleteProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      toast.success('Project deleted successfully')
    },
    onError: () => {
      toast.error('Failed to delete project')
    },
  })

  const handleDelete = (id: string, name: string) => {
    if (window.confirm(`Are you sure you want to delete "${name}"?`)) {
      deleteMutation.mutate(id)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-text-secondary-light dark:text-text-secondary-dark">
          Loading projects...
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-text-primary-light dark:text-text-primary-dark">
            Projects
          </h1>
          <p className="text-text-secondary-light dark:text-text-secondary-dark mt-1">
            Manage your M&A valuation projects
          </p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          <Plus className="h-4 w-4 mr-2" />
          New Project
        </Button>
      </div>

      {projects?.items.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <FolderOpen className="h-12 w-12 mx-auto text-text-secondary-light dark:text-text-secondary-dark mb-4" />
            <h3 className="text-lg font-medium text-text-primary-light dark:text-text-primary-dark mb-2">
              No projects yet
            </h3>
            <p className="text-text-secondary-light dark:text-text-secondary-dark mb-4">
              Get started by creating your first valuation project
            </p>
            <Button onClick={() => setShowCreateModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Project
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects?.items.map((project) => (
            <Card
              key={project.id}
              className="hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => navigate(`/projects/${project.id}`)}
            >
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-text-primary-light dark:text-text-primary-dark">
                    {project.name}
                  </h3>
                  {project.description && (
                    <p className="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">
                      {project.description}
                    </p>
                  )}
                </div>

                <div className="flex items-center justify-between">
                  <span
                    className={`px-2 py-1 text-xs rounded-full ${
                      project.status === 'active'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : project.status === 'draft'
                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                    }`}
                  >
                    {project.status}
                  </span>

                  <div className="flex space-x-2" onClick={(e) => e.stopPropagation()}>
                    <button
                      className="p-1 hover:bg-background-light dark:hover:bg-background-dark rounded"
                      onClick={() => navigate(`/projects/${project.id}`)}
                    >
                      <Edit className="h-4 w-4 text-text-secondary-light dark:text-text-secondary-dark" />
                    </button>
                    <button
                      className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded"
                      onClick={() => handleDelete(project.id, project.name)}
                    >
                      <Trash2 className="h-4 w-4 text-red-600 dark:text-red-400" />
                    </button>
                  </div>
                </div>

                <div className="text-xs text-text-secondary-light dark:text-text-secondary-dark">
                  Created {new Date(project.created_at).toLocaleDateString()}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {showCreateModal && (
        <CreateProjectModal onClose={() => setShowCreateModal(false)} />
      )}
    </div>
  )
}

function CreateProjectModal({ onClose }: { onClose: () => void }) {
  const queryClient = useQueryClient()
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [projectType, setProjectType] = useState('acquisition')

  const createMutation = useMutation({
    mutationFn: projectService.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      toast.success('Project created successfully')
      onClose()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create project')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate({ 
      name, 
      description,
      project_type: projectType
    })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <Card className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="space-y-4">
          <h2 className="text-xl font-bold text-text-primary-light dark:text-text-primary-dark">
            Create New Project
          </h2>

          <div>
            <label className="block text-sm font-medium text-text-primary-light dark:text-text-primary-dark mb-1">
              Project Name
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Permian Basin Acquisition"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary-light dark:text-text-primary-dark mb-1">
              Project Type
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              value={projectType}
              onChange={(e) => setProjectType(e.target.value)}
              required
            >
              <option value="acquisition">Acquisition</option>
              <option value="divestiture">Divestiture</option>
              <option value="jv">Joint Venture</option>
              <option value="farmout">Farm-out</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary-light dark:text-text-primary-dark mb-1">
              Description
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Evaluation of 50 wells in Midland Basin"
            />
          </div>

          <div className="flex space-x-3">
            <Button type="submit" loading={createMutation.isPending}>
              Create Project
            </Button>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}
