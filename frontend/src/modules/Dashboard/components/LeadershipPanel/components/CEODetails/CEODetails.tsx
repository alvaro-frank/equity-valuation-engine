import { useTranslation } from 'react-i18next';

export interface CEODetailsProps {
  ceoViewModel: { 
    cleanName?: string; 
    ownershipFormatted?: string | number | null; 
    title?: string;
  } | null;
}

export function CEODetails({ ceoViewModel }: CEODetailsProps) {
  const { t } = useTranslation();

  return (
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
  );
}
