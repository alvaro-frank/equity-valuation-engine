import { useTranslation } from 'react-i18next';
import { translateSector, translateIndustry } from '@/common/utils/translations';

export interface ChartHeaderProps {
  companyTicker: string;
  companyName?: string;
  sector: string;
  industry: string;
  benchmarkTicker: string;
}

export function ChartHeader({ companyTicker, companyName, sector, industry, benchmarkTicker }: ChartHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
      <div>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('sector_view.market_momentum', 'Relative Market Momentum (5Y)')}
        </h3>
        <p className="text-body-sm text-on-surface-variant">
          {t('sector_view.market_momentum_desc', 'Comparing Sector ETF performance vs Benchmark')}
        </p>
      </div>
      <div className="flex gap-2 cursor-default">
        {companyTicker && (
          <span className="text-xs px-2 py-1 bg-surface-container text-on-surface font-bold border border-outline-variant rounded">
            {companyName || companyTicker}
          </span>
        )}
        {industry && (
          <span className="text-xs px-2 py-1 bg-surface-container text-tertiary font-bold border border-outline-variant rounded">
            {translateIndustry(industry)}
          </span>
        )}
        {sector && (
          <span className="text-xs px-2 py-1 bg-surface-container text-primary font-bold border border-outline-variant rounded">
            {translateSector(sector)}
          </span>
        )}
        <span className="text-xs px-2 py-1 bg-surface-container font-bold border border-outline-variant rounded text-[var(--chart-benchmark)]">
          {benchmarkTicker || 'S&P 500'}
        </span>
      </div>
    </div>
  );
}
