import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { X, Upload, FileText, Loader2 } from 'lucide-react'
import { Button } from '../ui/Button'
import toast from 'react-hot-toast'
import { uploadService } from '@/services/uploadService'

interface FileUploadModalProps {
  projectId: number
  onClose: () => void
}

export default function FileUploadModal({ projectId, onClose }: FileUploadModalProps) {
  const [file, setFile] = useState<File | null>(null)
  const [fileType, setFileType] = useState<'production' | 'financial'>('production')
  const queryClient = useQueryClient()

  const uploadMutation = useMutation({
    mutationFn: (data: { file: File; fileType: 'production' | 'financial' }) =>
      uploadService.uploadFile(projectId, data.file, data.fileType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
      queryClient.invalidateQueries({ queryKey: ['files', projectId] })
      toast.success('File uploaded successfully')
      onClose()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to upload file')
    },
  })

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      toast.error('Please select a file')
      return
    }
    uploadMutation.mutate({ file, fileType })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            Upload Data File
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* File Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              File Type
            </label>
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setFileType('production')}
                className={`p-4 border-2 rounded-lg text-center transition-colors ${
                  fileType === 'production'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                }`}
              >
                <FileText className="w-8 h-8 mx-auto mb-2 text-blue-500" />
                <div className="font-medium">Production Data</div>
                <div className="text-xs text-gray-500 mt-1">Oil, Gas, Water volumes</div>
              </button>
              <button
                type="button"
                onClick={() => setFileType('financial')}
                className={`p-4 border-2 rounded-lg text-center transition-colors ${
                  fileType === 'financial'
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                    : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                }`}
              >
                <FileText className="w-8 h-8 mx-auto mb-2 text-green-500" />
                <div className="font-medium">Financial Data</div>
                <div className="text-xs text-gray-500 mt-1">Revenue, OPEX, CAPEX</div>
              </button>
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Select File (CSV or XLSX)
            </label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg hover:border-gray-400 dark:hover:border-gray-500 transition-colors">
              <div className="space-y-1 text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div className="flex text-sm text-gray-600 dark:text-gray-400">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none"
                  >
                    <span>Upload a file</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      className="sr-only"
                      accept=".csv,.xlsx,.xls"
                      onChange={handleFileChange}
                    />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">CSV or XLSX up to 10MB</p>
              </div>
            </div>
            {file && (
              <div className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Selected: <span className="font-medium">{file.name}</span>
              </div>
            )}
          </div>

          {/* Expected Format Info */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <h4 className="text-sm font-medium text-blue-900 dark:text-blue-300 mb-2">
              Expected Format:
            </h4>
            {fileType === 'production' ? (
              <div className="text-xs text-blue-800 dark:text-blue-400 space-y-1">
                <p>• <strong>date</strong>: YYYY-MM-DD</p>
                <p>• <strong>well_name</strong>: Well identifier</p>
                <p>• <strong>oil_volume</strong>: Barrels</p>
                <p>• <strong>gas_volume</strong>: MCF</p>
                <p>• <strong>water_volume</strong>: Barrels (optional)</p>
              </div>
            ) : (
              <div className="text-xs text-blue-800 dark:text-blue-400 space-y-1">
                <p>• <strong>date</strong>: YYYY-MM-DD</p>
                <p>• <strong>revenue</strong>: USD</p>
                <p>• <strong>opex</strong>: USD</p>
                <p>• <strong>capex</strong>: USD (optional)</p>
                <p>• <strong>taxes</strong>: USD (optional)</p>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={!file || uploadMutation.isPending}>
              {uploadMutation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Upload File
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
