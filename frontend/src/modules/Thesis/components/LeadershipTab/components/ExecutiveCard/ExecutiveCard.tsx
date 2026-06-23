import { useTranslation } from 'react-i18next';

export interface Executive { 
  name: string; 
  title: string; 
  ownership?: number | string | null; 
}

interface ExecutiveCardProps {
  exec: Executive;
}

export function ExecutiveCard({ exec }: ExecutiveCardProps) {
  const { t } = useTranslation();
  const cleanName = exec.name.replace(/^(Sr\.|Sra\.|Mr\.|Mrs\.|Ms\.|Miss\.|Dr\.|Prof\.)\s+/i, '');
  
  return (
    <div className="flex items-start gap-4 p-4 bg-surface-container-lowest border border-outline-variant/50 rounded-xl">
      <div className="flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2">
          <span className="text-sm text-on-surface font-bold leading-tight">{cleanName}</span>
          {exec.ownership != null ? (
            <span className="text-[10px] font-mono text-primary font-bold bg-primary/10 px-2 py-0.5 rounded border border-primary/20 shrink-0" title={`${t('dashboard.owned')} Shares`}>
              {Number(exec.ownership) < 0.1 ? Number(exec.ownership).toFixed(2) : Number(exec.ownership).toFixed(1)}% {t('dashboard.owned')}
            </span>
          ) : null}
        </div>
        <span className="text-xs text-on-surface-variant mt-1 leading-snug">{exec.title}</span>
      </div>
    </div>
  );
}
