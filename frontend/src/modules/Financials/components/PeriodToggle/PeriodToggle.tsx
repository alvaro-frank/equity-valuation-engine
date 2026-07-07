import { useTranslation } from 'react-i18next';

interface PeriodToggleProps {
  isQuarterly: boolean;
  onChange: (isQuarterly: boolean) => void;
}

export function PeriodToggle({ isQuarterly, onChange }: PeriodToggleProps) {
  const { t } = useTranslation();
  return (
    <div className="flex items-center bg-surface-container border border-outline-variant rounded-lg p-1">
      <button
        onClick={() => onChange(false)}
        className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${!isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
      >
        {t('financials.annual', 'Annual')}
      </button>
      <button
        onClick={() => onChange(true)}
        className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
      >
        {t('financials.quarterly', 'Quarterly')}
      </button>
    </div>
  );
}
