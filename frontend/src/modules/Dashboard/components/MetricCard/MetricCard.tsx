import React from 'react';

interface MetricCardProps {
  label: string;
  value: string;
  icon: string;
  subValue?: string;
  subValueColor?: string;
  children?: React.ReactNode;
}

export function MetricCard({ 
  label, 
  value, 
  icon, 
  subValue, 
  subValueColor = 'text-on-surface-variant',
  children 
}: MetricCardProps) {
  return (
    <div className="bg-surface-container-low border border-outline-variant p-3 flex flex-col justify-between group hover:bg-surface-container transition-colors">
      <div className="flex justify-between items-start">
        <span className="font-label-caps text-label-caps text-on-surface-variant">{label}</span>
        <span className="material-symbols-outlined text-outline text-[16px]">{icon}</span>
      </div>
      <div className="mt-2">
        <p className="font-data-mono text-[20px] text-on-surface">{value}</p>
        {subValue && (
          <p className={`text-[10px] mt-1 ${subValueColor}`}>{subValue}</p>
        )}
        {children}
      </div>
    </div>
  );
}
