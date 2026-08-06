import type { ReactNode } from 'react';
import { InfoTooltip } from '../InfoTooltip';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  tooltipText?: ReactNode;
  children: ReactNode;
}

export function ChartCard({ title, subtitle, tooltipText, children }: ChartCardProps) {
  return (
    <div className="flex flex-col bg-surface-container-low border border-outline-variant rounded-xl p-5 shadow-sm">
      <div className="mb-4 flex items-start justify-between">
        <div>
          <h3 className="text-base font-semibold text-on-surface">{title}</h3>
          {subtitle && (
            <p className="text-sm text-on-surface-variant mt-1">{subtitle}</p>
          )}
        </div>
        {tooltipText && <InfoTooltip content={tooltipText} />}
      </div>
      <div className="flex-1 w-full relative">
        {children}
      </div>
    </div>
  );
}
