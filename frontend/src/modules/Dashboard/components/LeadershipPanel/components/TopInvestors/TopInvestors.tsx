import { useTranslation } from 'react-i18next';

interface TopInvestorsProps {
  majorShareholders?: Record<string, string | number>;
}

export function TopInvestors({ majorShareholders }: TopInvestorsProps) {
  const { t } = useTranslation();

  if (!majorShareholders || Object.keys(majorShareholders).length === 0) {
    return null;
  }

  return (
    <div className="mt-auto pt-4 border-t border-outline-variant/50">
      <p className="font-label-caps text-label-caps text-on-surface-variant mb-3">{t('company_profile.top_investors')}</p>
      <div className="flex flex-wrap gap-2">
        {Object.entries(majorShareholders).map(([investor, pct]) => (
          <span key={investor} className="bg-surface-container text-on-surface-variant text-[11px] px-2 py-1 rounded border border-outline-variant flex items-center">
            <span className="font-medium text-on-surface mr-1.5">{investor}</span>
            <span className="font-mono opacity-80">
              {Number(pct).toFixed(2)}%
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}
