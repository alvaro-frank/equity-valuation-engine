import { useTranslation } from 'react-i18next';

interface TrendingTickersProps {
  onSelect: (symbol: string, name: string) => void;
}

export function TrendingTickers({ onSelect }: TrendingTickersProps) {
  const { t } = useTranslation();
  const suggestedTickers = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'MSFT', name: 'Microsoft Corp.' },
    { symbol: 'NVDA', name: 'NVIDIA Corp.' },
    { symbol: 'TSLA', name: 'Tesla Inc.' },
    { symbol: 'AMZN', name: 'Amazon.com' },
  ];

  return (
    <div className="mt-12 w-full">
      <p className="text-on-surface-variant font-label-caps text-label-caps mb-4 text-center">
        {t('search.trending_tickers')}
      </p>
      <div className="flex flex-wrap justify-center gap-3">
        {suggestedTickers.map((ticker) => (
          <button
            key={ticker.symbol}
            onClick={() => onSelect(ticker.symbol, ticker.name)}
            className="flex items-center gap-2 px-4 py-2 bg-surface-container-low border border-outline-variant hover:border-primary hover:bg-surface-container-high rounded-full transition-all group"
          >
            <span className="font-bold text-primary">{ticker.symbol}</span>
            <span className="text-on-surface-variant text-sm group-hover:text-on-surface transition-colors">
              {ticker.name}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
