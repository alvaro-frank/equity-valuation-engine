import { useTranslation } from 'react-i18next';
import { TrendingBadge } from '../TrendingBadge';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { formatLargeCurrency } from '@/common/utils/formatters';
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
      <div className="text-right flex flex-col items-end justify-center">
        <span className="font-display-lg text-3xl font-bold text-primary leading-none">
          {formatLargeCurrency(quantData?.ticker?.current_price)}
        </span>
        {quantData?.ticker?.regular_market_change != null ? (
          <span className={`text-[12px] font-bold mt-1.5 flex items-center gap-0.5 ${quantData.ticker.regular_market_change >= 0 ? 'text-green-500' : 'text-error'}`}>
            <span className="material-symbols-outlined text-[14px]">
              {quantData.ticker.regular_market_change >= 0 ? 'arrow_upward' : 'arrow_downward'}
            </span>
            ${Math.abs(quantData.ticker.regular_market_change).toFixed(2)} ({Math.abs(quantData.ticker.regular_market_change_percent || 0).toFixed(2)}%)
          </span>
        ) : (
          <span className="text-on-surface-variant text-[11px] font-medium mt-1 tracking-wide">{t('company_profile.live_pricing')}</span>
        )}
      </div>
    </div>
  );
}
