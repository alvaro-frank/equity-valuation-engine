import { useTranslation } from 'react-i18next';
import type { QualitativeValuationResult } from '@/common/types/valuation';

interface LeadershipPanelProps {
  qualData?: QualitativeValuationResult;
  ceoViewModel: { cleanName?: string; ownershipFormatted?: string | number | null; title?: string } | null;
}

export function LeadershipPanel({ qualData, ceoViewModel }: LeadershipPanelProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-outline-variant">
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">{t('company_profile.leadership')}</h3>
      </div>
      <div className="p-4 flex-1 flex flex-col space-y-6">
        <div className="flex items-center gap-4 shrink-0">
          <div>
            <div className="flex items-center gap-2">
              <p className="text-on-surface font-semibold line-clamp-1">{ceoViewModel?.cleanName || 'Unknown'}</p>
              {ceoViewModel?.ownershipFormatted != null ? (
                <span className="bg-primary/10 border border-primary/20 text-primary text-[10px] font-bold px-2 py-0.5 rounded-sm shrink-0" title={`${ceoViewModel.title} Skin in the Game`}>
                  {ceoViewModel.ownershipFormatted}% {t('dashboard.owned')}
                </span>
              ) : null}
            </div>
            <p className="text-on-surface-variant text-[11px] uppercase tracking-tighter">{ceoViewModel?.title || t('company_header.ceo')}</p>
          </div>
        </div>
        <div className="mt-4 flex-1 flex flex-col overflow-y-auto custom-scrollbar pr-2">
          <p className="text-body-sm text-on-surface-variant leading-relaxed mb-4" title={qualData?.management_insights}>{qualData?.management_insights || 'Analyzing leadership...'}</p>
          
          {qualData?.major_shareholders && Object.keys(qualData.major_shareholders).length > 0 ? (
            <div className="mt-auto pt-4 border-t border-outline-variant/50">
              <p className="font-label-caps text-label-caps text-on-surface-variant mb-3">{t('company_profile.top_investors')}</p>
              <div className="flex flex-wrap gap-2">
                {Object.entries(qualData.major_shareholders).map(([investor, pct]) => (
                  <span key={investor} className="bg-surface-container text-on-surface-variant text-[11px] px-2 py-1 rounded border border-outline-variant flex items-center">
                    <span className="font-medium text-on-surface mr-1.5">{investor}</span>
                    <span className="font-mono opacity-80">
                      {Number(pct).toFixed(2)}%
                    </span>
                  </span>
                ))}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
