import { useTranslation } from 'react-i18next';
import { RiskCard } from '../RiskCard';

interface RisksListProps {
  risks?: Record<string, string>;
}

export function RisksList({ risks }: RisksListProps) {
  const { t } = useTranslation();
  const hasData = Object.keys(risks || {}).length > 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {hasData ? (
        Object.entries(risks!).map(([risk, description], index) => (
          <RiskCard key={risk} risk={risk} description={description} index={index} />
        ))
      ) : (
        <p className="text-sm text-on-surface-variant italic p-4 col-span-2">{t('thesis_view.no_data')}</p>
      )}
    </div>
  );
}
