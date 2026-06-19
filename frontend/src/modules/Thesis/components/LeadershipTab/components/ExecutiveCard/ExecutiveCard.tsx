import { useTranslation } from 'react-i18next';

export interface Executive { 
  name: string; 
  title: string; 
  ownership?: number | string | null; 
}

const getInitials = (name: string) => {
  if (!name) return '?';
  const parts = name.replace(/^(Mr\.|Ms\.|Mrs\.|Dr\.)\s+/i, '').trim().split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

interface ExecutiveCardProps {
  exec: Executive;
}

export function ExecutiveCard({ exec }: ExecutiveCardProps) {
  const { t } = useTranslation();
  const cleanName = exec.name.replace(/^(Sr\.|Sra\.|Mr\.|Mrs\.|Ms\.|Miss\.|Dr\.|Prof\.)\s+/i, '');
  
  return (
    <div className="flex items-start gap-4 p-4 bg-surface-container-lowest border border-outline-variant/50 hover:bg-surface-container-low transition-colors duration-200 rounded-xl group">
      <div className="w-11 h-11 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-bold text-sm shrink-0 group-hover:bg-primary/20 transition-colors">
        {getInitials(cleanName)}
      </div>
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
