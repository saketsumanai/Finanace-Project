import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { Plus, Trash2, Save } from 'lucide-react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Card } from '../ui/Card'
import { CreateSynergyModelData } from '@/services/modelingService'

interface SynergyModelFormProps {
  onSubmit: (data: CreateSynergyModelData) => Promise<void>
  onCancel?: () => void
}

const SYNERGY_CATEGORIES = [
  { value: 'operational_overhead', label: 'Operational Overhead' },
  { value: 'procurement_efficiency', label: 'Procurement Efficiency' },
  { value: 'workforce_consolidation', label: 'Workforce Consolidation' },
  { value: 'shared_infrastructure', label: 'Shared Infrastructure' },
]

const STANDARD_SCHEDULES = {
  aggressive: [
    { year: 1, percentage: 0.50 },
    { year: 2, percentage: 0.85 },
    { year: 3, percentage: 1.00 },
  ],
  standard: [
    { year: 1, percentage: 0.25 },
    { year: 2, percentage: 0.60 },
    { year: 3, percentage: 0.85 },
    { year: 4, percentage: 1.00 },
  ],
  conservative: [
    { year: 1, percentage: 0.15 },
    { year: 2, percentage: 0.40 },
    { year: 3, percentage: 0.65 },
    { year: 4, percentage: 0.85 },
    { year: 5, percentage: 1.00 },
  ],
}

export default function SynergyModelForm({ onSubmit, onCancel }: SynergyModelFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const { register, control, handleSubmit, setValue, formState: { errors } } = useForm<CreateSynergyModelData>({
    defaultValues: {
      category: 'operational_overhead',
      description: '',
      target_value: 0,
      realization_schedule: STANDARD_SCHEDULES.standard,
    },
  })

  const { fields, append, remove, replace } = useFieldArray({
    control,
    name: 'realization_schedule',
  })

  const handleFormSubmit = async (data: CreateSynergyModelData) => {
    setIsSubmitting(true)
    try {
      await onSubmit(data)
    } finally {
      setIsSubmitting(false)
    }
  }

  const applyStandardSchedule = (type: 'aggressive' | 'standard' | 'conservative') => {
    replace(STANDARD_SCHEDULES[type])
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <Card>
        <h3 className="text-lg font-semibold mb-4">Synergy Details</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Synergy Category</label>
            <select
              {...register('category', { required: 'Category is required' })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {SYNERGY_CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
            {errors.category && (
              <p className="text-red-500 text-sm mt-1">{errors.category.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <textarea
              {...register('description')}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe the synergy opportunity..."
            />
          </div>

          <Input
            label="Target Annual Value ($)"
            type="number"
            {...register('target_value', { 
              valueAsNumber: true, 
              required: 'Target value is required',
              min: { value: 0, message: 'Must be positive' }
            })}
            error={errors.target_value?.message}
            placeholder="2000000"
          />
        </div>
      </Card>

      <Card>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Realization Schedule</h3>
          <div className="flex gap-2">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => applyStandardSchedule('aggressive')}
            >
              Aggressive
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => applyStandardSchedule('standard')}
            >
              Standard
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => applyStandardSchedule('conservative')}
            >
              Conservative
            </Button>
          </div>
        </div>

        <div className="mb-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
          <p className="font-medium mb-1">Standard Schedules:</p>
          <ul className="list-disc list-inside space-y-1">
            <li><strong>Aggressive:</strong> 50% → 85% → 100% (3 years)</li>
            <li><strong>Standard:</strong> 25% → 60% → 85% → 100% (4 years)</li>
            <li><strong>Conservative:</strong> 15% → 40% → 65% → 85% → 100% (5 years)</li>
          </ul>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium">Year-by-Year Realization</label>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => append({ year: fields.length + 1, percentage: 0 })}
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Year
            </Button>
          </div>
          
          {fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 items-start">
              <Input
                label={index === 0 ? 'Year' : ''}
                type="number"
                {...register(`realization_schedule.${index}.year` as const, { 
                  valueAsNumber: true,
                  required: 'Year is required'
                })}
                placeholder="Year"
                className="w-24"
              />
              <Input
                label={index === 0 ? 'Percentage (%)' : ''}
                type="number"
                step="0.01"
                {...register(`realization_schedule.${index}.percentage` as const, { 
                  valueAsNumber: true,
                  required: 'Percentage is required',
                  min: { value: 0, message: 'Min 0%' },
                  max: { value: 1, message: 'Max 100%' }
                })}
                placeholder="0.25"
              />
              {fields.length > 1 && (
                <button
                  type="button"
                  onClick={() => remove(index)}
                  className="text-red-500 hover:text-red-700 mt-6"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <strong>Note:</strong> Percentage values should be between 0 and 1 (e.g., 0.25 for 25%, 1.00 for 100%)
          </p>
        </div>
      </Card>

      {/* Form Actions */}
      <div className="flex justify-end gap-3">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" disabled={isSubmitting}>
          <Save className="w-4 h-4 mr-2" />
          {isSubmitting ? 'Saving...' : 'Save Synergy Model'}
        </Button>
      </div>
    </form>
  )
}
