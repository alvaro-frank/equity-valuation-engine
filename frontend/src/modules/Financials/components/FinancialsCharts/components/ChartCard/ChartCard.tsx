import type { ReactNode } from 'react';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export function ChartCard({ title, subtitle, children }: ChartCardProps) {
  return (
    <div className="flex flex-col bg-surface-container-low border border-outline-variant rounded-xl p-5 shadow-sm">
      <div className="mb-4">
        <h3 className="text-base font-semibold text-on-surface">{title}</h3>
        {subtitle && (
          <p className="text-sm text-on-surface-variant mt-1">{subtitle}</p>
        )}
      </div>
      <div className="flex-1 w-full relative">
        {children}
      </div>
    </div>
  );
}
