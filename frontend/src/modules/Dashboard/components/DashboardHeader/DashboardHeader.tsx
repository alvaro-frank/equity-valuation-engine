import { useTranslation } from 'react-i18next';
import { TrendingBadge } from '../TrendingBadge';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { PriceDisplay } from './components/PriceDisplay';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';

interface DashboardHeaderProps {
  ticker: string;
  quantData?: QuantitativeValuationResult;
  qualData?: QualitativeValuationResult;
  onSearch?: (ticker: string) => void;
}

export function DashboardHeader({ ticker, quantData, qualData, onSearch }: DashboardHeaderProps) {
  const { t } = useTranslation();

  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-1">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">
            {qualData?.ticker?.name || ticker} ({ticker})
          </h1>
          <div className="flex gap-2">
            <TrendingBadge
              type="sector"
              label={t('dashboard.sector')}
              value={translateSector(qualData?.ticker?.sector)}
              queryKey={qualData?.ticker?.sector_key || quantData?.ticker?.sector_key}
              currentTicker={ticker}
              onSelectTicker={onSearch || (() => {})}
            />
            <TrendingBadge
              type="industry"
              label={t('dashboard.industry')}
              value={translateIndustry(qualData?.ticker?.industry)}
              queryKey={qualData?.ticker?.industry_key || quantData?.ticker?.industry_key}
              currentTicker={ticker}
              onSelectTicker={onSearch || (() => {})}
            />
          </div>
        </div>
      </div>
      <PriceDisplay 
        currentPrice={quantData?.ticker?.current_price}
        change={quantData?.ticker?.regular_market_change}
        changePercent={quantData?.ticker?.regular_market_change_percent}
      />
    </div>
  );
}
