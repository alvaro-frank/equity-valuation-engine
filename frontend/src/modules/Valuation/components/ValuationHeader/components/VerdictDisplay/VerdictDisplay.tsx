import { useTranslation } from 'react-i18next';

export interface VerdictDisplayProps {
  currentPrice: number;
  intrinsicValue: number;
}

export function VerdictDisplay({ currentPrice, intrinsicValue }: VerdictDisplayProps) {
  const { t } = useTranslation();
  
  const safeCurrentPrice = Number(currentPrice) || 0;
  const safeIntrinsicValue = Number(intrinsicValue) || 0;
  const marginOfSafety = safeCurrentPrice > 0 ? ((safeIntrinsicValue - safeCurrentPrice) / safeCurrentPrice) * 100 : 0;
  const isUndervalued = marginOfSafety > 0;

  return (
    <>
      <div className="flex flex-col items-end">
        <span className="text-label-sm text-on-surface-variant">{t('valuation.current_price', 'Current Price')}</span>
        <span className="text-4xl font-bold text-on-surface">${safeCurrentPrice.toFixed(2)}</span>
      </div>

      <div className="w-px h-14 bg-outline-variant hidden sm:block"></div>

      <div className="flex flex-col items-end">
        <span className="text-label-sm text-on-surface-variant">{t('valuation.intrinsic_value', 'Intrinsic Value')}</span>
        <div className="flex items-center gap-3">
          <span className="text-4xl font-bold tracking-tight text-on-surface">
            ${safeIntrinsicValue.toFixed(2)}
          </span>
          <span
            className={`text-sm font-bold px-2 py-1 rounded border border-outline-variant ${isUndervalued ? 'text-secondary' : 'text-error'
              }`}
          >
            {isUndervalued ? '+' : ''}{marginOfSafety.toFixed(1)}%
          </span>
        </div>
      </div>
    </>
  );
}
