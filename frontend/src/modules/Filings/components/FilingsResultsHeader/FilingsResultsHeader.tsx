import { useTranslation } from 'react-i18next';

interface FilingsResultsHeaderProps {
  onReset: () => void;
}

export function FilingsResultsHeader({ onReset }: FilingsResultsHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="flex items-center gap-3 mb-4">
      <h3 className="text-lg font-bold text-on-surface">{t('filings.results')}</h3>
      <button 
        onClick={onReset} 
        className="p-1.5 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant transition-colors flex items-center justify-center"
        title={t('filings.analyze_another')}
      >
        <span className="material-symbols-outlined text-[18px]">refresh</span>
      </button>
    </div>
  );
}
