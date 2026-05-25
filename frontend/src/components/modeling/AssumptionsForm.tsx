import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { Plus, Trash2, Save } from 'lucide-react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Card } from '../ui/Card'
import { CreateAssumptionsData, PriceForecast, CapexScheduleItem } from '@/services/modelingService'

interface AssumptionsFormProps {
  projectId: string
  initialData?: Partial<CreateAssumptionsData>
  onSubmit: (data: CreateAssumptionsData) => Promise<void>
  onCancel?: () => void
}

export default function AssumptionsForm({ projectId, initialData, onSubmit, onCancel }: AssumptionsFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const { register, control, handleSubmit, watch, formState: { errors } } = useForm<CreateAssumptionsData>({
    defaultValues: {
      project_id: projectId,
      name: initialData?.name || '',
      version: initialData?.version || 1,
      decline_curve_type: initialData?.decline_curve_type || 'hyperbolic',
      decline_rate: initialData?.decline_rate || 0.15,
      hyperbolic_b: initialData?.hyperbolic_b || 0.5,
      oil_price_forecast: initialData?.oil_price_forecast || [{ year: 1, price: 70 }],
      gas_price_forecast: initialData?.gas_price_forecast || [{ year: 1, price: 3.5 }],
      opex_inflation_rate: initialData?.opex_inflation_rate || 0.03,
      capex_schedule: initialData?.capex_schedule || [],
      transportation_cost_per_unit: initialData?.transportation_cost_per_unit || 2.5,
      ga_annual: initialData?.ga_annual || 1000000,
      purchase_price: initialData?.purchase_price || 50000000,
      debt_amount: initialData?.debt_amount || 0,
      equity_amount: initialData?.equity_amount || 0,
      discount_rate: initialData?.discount_rate || 0.12,
      tax_rate: initialData?.tax_rate || 0.21,
      exit_multiple: initialData?.exit_multiple || 5.5,
      forecast_years: initialData?.forecast_years || 20,
    },
  })

  const declineCurveType = watch('decline_curve_type')

  const { fields: oilPriceFields, append: appendOilPrice, remove: removeOilPrice } = useFieldArray({
    control,
    name: 'oil_price_forecast',
  })

  const { fields: gasPriceFields, append: appendGasPrice, remove: removeGasPrice } = useFieldArray({
    control,
    name: 'gas_price_forecast',
  })

  const { fields: capexFields, append: appendCapex, remove: removeCapex } = useFieldArray({
    control,
    name: 'capex_schedule',
  })

  const handleFormSubmit = async (data: CreateAssumptionsData) => {
    setIsSubmitting(true)
    try {
      await onSubmit(data)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      {/* Basic Information */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Basic Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Assumptions Name"
            {...register('name', { required: 'Name is required' })}
            error={errors.name?.message}
            placeholder="e.g., Base Case Assumptions"
          />
          <Input
            label="Version"
            type="number"
            {...register('version', { valueAsNumber: true, min: 1 })}
            error={errors.version?.message}
          />
        </div>
      </Card>

      {/* Production Assumptions */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Production Assumptions</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Decline Curve Type</label>
            <select
              {...register('decline_curve_type')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="exponential">Exponential</option>
              <option value="hyperbolic">Hyperbolic</option>
              <option value="harmonic">Harmonic</option>
            </select>
          </div>
          
          <Input
            label="Decline Rate (%)"
            type="number"
            step="0.01"
            {...register('decline_rate', { valueAsNumber: true, min: 0, max: 1 })}
            error={errors.decline_rate?.message}
            placeholder="0.15"
          />
          
          {declineCurveType === 'hyperbolic' && (
            <Input
              label="Hyperbolic b-factor"
              type="number"
              step="0.01"
              {...register('hyperbolic_b', { valueAsNumber: true, min: 0, max: 1 })}
              error={errors.hyperbolic_b?.message}
              placeholder="0.5"
            />
          )}
        </div>

        {/* Oil Price Forecast */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-3">
            <label className="block text-sm font-medium">Oil Price Forecast ($/bbl)</label>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => appendOilPrice({ year: oilPriceFields.length + 1, price: 70 })}
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Year
            </Button>
          </div>
          <div className="space-y-2">
            {oilPriceFields.map((field, index) => (
              <div key={field.id} className="flex gap-2">
                <Input
                  label={index === 0 ? 'Year' : ''}
                  type="number"
                  {...register(`oil_price_forecast.${index}.year` as const, { valueAsNumber: true })}
                  placeholder="Year"
                  className="w-24"
                />
                <Input
                  label={index === 0 ? 'Price' : ''}
                  type="number"
                  step="0.01"
                  {...register(`oil_price_forecast.${index}.price` as const, { valueAsNumber: true })}
                  placeholder="Price"
                />
                {oilPriceFields.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeOilPrice(index)}
                    className="text-red-500 hover:text-red-700 mt-6"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Gas Price Forecast */}
        <div>
          <div className="flex justify-between items-center mb-3">
            <label className="block text-sm font-medium">Gas Price Forecast ($/MCF)</label>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => appendGasPrice({ year: gasPriceFields.length + 1, price: 3.5 })}
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Year
            </Button>
          </div>
          <div className="space-y-2">
            {gasPriceFields.map((field, index) => (
              <div key={field.id} className="flex gap-2">
                <Input
                  label={index === 0 ? 'Year' : ''}
                  type="number"
                  {...register(`gas_price_forecast.${index}.year` as const, { valueAsNumber: true })}
                  placeholder="Year"
                  className="w-24"
                />
                <Input
                  label={index === 0 ? 'Price' : ''}
                  type="number"
                  step="0.01"
                  {...register(`gas_price_forecast.${index}.price` as const, { valueAsNumber: true })}
                  placeholder="Price"
                />
                {gasPriceFields.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeGasPrice(index)}
                    className="text-red-500 hover:text-red-700 mt-6"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Cost Assumptions */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Cost Assumptions</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Input
            label="OPEX Inflation Rate (%)"
            type="number"
            step="0.01"
            {...register('opex_inflation_rate', { valueAsNumber: true })}
            error={errors.opex_inflation_rate?.message}
            placeholder="0.03"
          />
          <Input
            label="Transportation Cost per BOE ($)"
            type="number"
            step="0.01"
            {...register('transportation_cost_per_unit', { valueAsNumber: true })}
            error={errors.transportation_cost_per_unit?.message}
            placeholder="2.5"
          />
          <Input
            label="Annual G&A ($)"
            type="number"
            {...register('ga_annual', { valueAsNumber: true })}
            error={errors.ga_annual?.message}
            placeholder="1000000"
          />
        </div>

        {/* CAPEX Schedule */}
        <div>
          <div className="flex justify-between items-center mb-3">
            <label className="block text-sm font-medium">CAPEX Schedule</label>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => appendCapex({ year: 1, amount: 0 })}
            >
              <Plus className="w-4 h-4 mr-1" />
              Add CAPEX
            </Button>
          </div>
          <div className="space-y-2">
            {capexFields.map((field, index) => (
              <div key={field.id} className="flex gap-2">
                <Input
                  label={index === 0 ? 'Year' : ''}
                  type="number"
                  {...register(`capex_schedule.${index}.year` as const, { valueAsNumber: true })}
                  placeholder="Year"
                  className="w-24"
                />
                <Input
                  label={index === 0 ? 'Amount ($)' : ''}
                  type="number"
                  {...register(`capex_schedule.${index}.amount` as const, { valueAsNumber: true })}
                  placeholder="Amount"
                />
                <button
                  type="button"
                  onClick={() => removeCapex(index)}
                  className="text-red-500 hover:text-red-700 mt-6"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Deal Assumptions */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Deal Assumptions</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Purchase Price ($)"
            type="number"
            {...register('purchase_price', { valueAsNumber: true, required: 'Purchase price is required' })}
            error={errors.purchase_price?.message}
            placeholder="50000000"
          />
          <Input
            label="Debt Amount ($)"
            type="number"
            {...register('debt_amount', { valueAsNumber: true })}
            error={errors.debt_amount?.message}
            placeholder="0"
          />
          <Input
            label="Equity Amount ($)"
            type="number"
            {...register('equity_amount', { valueAsNumber: true })}
            error={errors.equity_amount?.message}
            placeholder="0"
          />
          <Input
            label="Discount Rate (WACC) (%)"
            type="number"
            step="0.01"
            {...register('discount_rate', { valueAsNumber: true })}
            error={errors.discount_rate?.message}
            placeholder="0.12"
          />
          <Input
            label="Tax Rate (%)"
            type="number"
            step="0.01"
            {...register('tax_rate', { valueAsNumber: true })}
            error={errors.tax_rate?.message}
            placeholder="0.21"
          />
          <Input
            label="Exit Multiple (x EBITDA)"
            type="number"
            step="0.1"
            {...register('exit_multiple', { valueAsNumber: true })}
            error={errors.exit_multiple?.message}
            placeholder="5.5"
          />
          <Input
            label="Forecast Years"
            type="number"
            {...register('forecast_years', { valueAsNumber: true })}
            error={errors.forecast_years?.message}
            placeholder="20"
          />
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
          {isSubmitting ? 'Saving...' : 'Save Assumptions'}
        </Button>
      </div>
    </form>
  )
}
