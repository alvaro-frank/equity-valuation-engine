
export interface CompetitiveForceCardProps {
  icon: string;
  title: string;
  data: Record<string, string>;
  className?: string;
}

export function CompetitiveForceCard({ icon, title, data, className = '' }: CompetitiveForceCardProps) {
  if (!data) return null;
  
  return (
    <div className={`bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4 ${className}`}>
      <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
        <span className="material-symbols-outlined text-primary text-[28px]">{icon}</span>
        <h3 className="font-display-sm text-xl text-on-surface">{title}</h3>
      </div>
      <div className="space-y-4">
        {Object.entries(data).map(([factor, analysis]) => (
          <div key={factor}>
            <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
            <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
