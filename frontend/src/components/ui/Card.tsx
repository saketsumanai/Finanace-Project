import React from 'react'
import { cn } from '@/utils/cn'

interface CardProps {
  title?: string
  subtitle?: string
  children: React.ReactNode
  actions?: React.ReactNode
  className?: string
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  children,
  actions,
  className
}) => {
  return (
    <div className={cn('card', className)}>
      {(title || actions) && (
        <div className="px-6 py-4 border-b border-border-light dark:border-border-dark flex justify-between items-center">
          <div>
            {title && (
              <h3 className="text-lg font-semibold text-text-primary-light dark:text-text-primary-dark">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">
                {subtitle}
              </p>
            )}
          </div>
          {actions && <div>{actions}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  )
}
