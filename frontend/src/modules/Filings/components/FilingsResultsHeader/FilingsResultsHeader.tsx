import { useTranslation } from 'react-i18next';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { formatDateString } from '@/common/utils/formatters';

interface FilingsResultsHeaderProps {
  onReset?: () => void;
  ticker: string;
  name?: string;
  sector?: string;
  industry?: string;
  periodEndDate?: string;
}

export function FilingsResultsHeader({ onReset, ticker, name, sector, industry, periodEndDate }: FilingsResultsHeaderProps) {
  const { t, i18n } = useTranslation();

  const formattedDate = formatDateString(periodEndDate, i18n.language);

  return (
    <div className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 pt-6 pb-4 mb-6 flex items-end justify-between border-b border-outline-variant/20 -mx-4 px-4 sm:-mx-8 sm:px-8">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{name || ticker}</h1>
          <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider mt-1">
            {t('nav.filings')}
          </span>
        </div>
        {sector && industry ? (
          <p className="text-body-sm text-on-surface-variant mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {translateSector(sector)} / {translateIndustry(industry)}
          </p>
        ) : null}
      </div>
      <div className="flex items-center gap-4 mb-1">
        {periodEndDate ? (
          <div className="flex items-center gap-2 text-on-surface-variant bg-surface-container-low px-3 py-1.5 rounded-sm border border-outline-variant">
            <span className="material-symbols-outlined text-[16px]">calendar_month</span>
            <span className="text-sm font-medium">{t('filings.period_ended')}: {formattedDate}</span>
          </div>
        ) : null}
        {onReset ? (
          <button 
            onClick={onReset} 
            className="p-2 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant transition-colors flex items-center justify-center"
            title={t('filings.analyze_another')}
          >
            <span className="material-symbols-outlined text-[20px]">arrow_back</span>
          </button>
        ) : null}
      </div>
    </div>
  );
}
