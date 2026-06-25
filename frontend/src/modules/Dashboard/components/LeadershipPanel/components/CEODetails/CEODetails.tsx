import { useTranslation } from 'react-i18next';

export interface CEODetailsProps {
  ceoViewModel: { 
    cleanName?: string; 
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
        </div>
        <p className="text-on-surface-variant text-[11px] uppercase tracking-tighter">{ceoViewModel?.title || t('company_header.ceo')}</p>
      </div>
    </div>
  );
}
