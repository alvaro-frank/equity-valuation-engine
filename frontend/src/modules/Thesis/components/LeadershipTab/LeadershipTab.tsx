import { useTranslation } from 'react-i18next';

const getInitials = (name: string) => {
  if (!name) return '?';
  const parts = name.replace(/^(Mr\.|Ms\.|Mrs\.|Dr\.)\s+/i, '').trim().split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

// --- Sub-Components (Rule 2.23, 2.30, 2.31) ---

interface Executive { name: string; title: string; ownership?: number | string | null; }
function ExecutiveCard({ exec }: { exec: Executive }) {
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

function ShareholderRow({ investor, pct }: { investor: string; pct: number }) {
  return (
    <div className="flex items-center justify-between p-3 bg-surface-container-lowest border border-outline-variant/50 rounded-lg">
      <span className="text-sm text-on-surface-variant font-medium line-clamp-1 pr-2">{investor}</span>
      <span className="text-sm font-mono text-on-surface font-bold bg-surface-container-high px-2 py-0.5 rounded border border-outline-variant/50 shrink-0">
        {Number(pct).toFixed(2)}%
      </span>
    </div>
  );
}

function ExecutivesSection({ executives }: { executives: Executive[] }) {
  const { t } = useTranslation();
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-secondary">groups</span>
        {t('company_profile.leadership')}
      </h3>
      <div className="space-y-2">
        {executives?.map((exec, idx) => (
          <ExecutiveCard key={idx} exec={exec} />
        ))}
      </div>
    </div>
  );
}

function ShareholdersSection({ shareholders }: { shareholders: Record<string, number> }) {
  const { t } = useTranslation();
  const hasData = Object.keys(shareholders || {}).length > 0;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-secondary">pie_chart</span>
        {t('thesis_view.shareholders_title')}
      </h3>
      <div className="space-y-2">
        {hasData ? (
          Object.entries(shareholders).map(([investor, pct]) => (
            <ShareholderRow key={investor} investor={investor} pct={pct as number} />
          ))
        ) : (
          <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
        )}
      </div>
    </div>
  );
}

function LeadershipInsights({ content }: { content: string }) {
  const { t } = useTranslation();
  return (
    <div className="lg:col-span-2">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">insights</span>
        {t('thesis_view.leadership_title')}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 min-h-[400px]">
        <p>{content}</p>
      </div>
    </div>
  );
}

// --- Main Component ---

interface LeadershipTabProps {
  qualData: Record<string, unknown>;
}

export function LeadershipTab({ qualData }: LeadershipTabProps) {
  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <ExecutivesSection executives={qualData?.key_executives} />
          <ShareholdersSection shareholders={qualData?.major_shareholders || {}} />
        </div>
        
        <LeadershipInsights content={qualData?.management_insights} />
      </div>
    </div>
  );
}
