import { useTranslation } from 'react-i18next';
import { formatStockPrice } from '@/common/utils/formatters';

interface PriceDisplayProps {
  currentPrice?: number | null;
  change?: number | null;
  changePercent?: number | null;
}

export function PriceDisplay({ currentPrice, change, changePercent }: PriceDisplayProps) {
  const { t } = useTranslation();

  return (
    <div className="text-right flex flex-col items-end justify-center">
      <span className="font-display-lg text-3xl font-bold text-primary leading-none">
        {formatStockPrice(currentPrice)}
      </span>
      {change != null ? (
        <span className={`text-[12px] font-bold mt-1.5 flex items-center gap-0.5 ${change >= 0 ? 'text-green-500' : 'text-error'}`}>
          <span className="material-symbols-outlined text-[14px]">
            {change >= 0 ? 'arrow_upward' : 'arrow_downward'}
          </span>
          ${Math.abs(change).toFixed(2)} ({Math.abs(changePercent || 0).toFixed(2)}%)
        </span>
      ) : (
        <span className="text-on-surface-variant text-[11px] font-medium mt-1 tracking-wide">
          {t('company_profile.live_pricing')}
        </span>
      )}
    </div>
  );
}
