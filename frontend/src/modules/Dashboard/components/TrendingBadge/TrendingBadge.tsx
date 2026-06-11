import { useTranslation } from 'react-i18next';
import { SearchResultItem } from '@/common/components/SearchResultItem';
import { useTrendingBadge } from './useTrendingBadge';

// --- Types ---
interface TrendingBadgeProps {
  label: string;
  value: string;
  type: 'sector' | 'industry';
  queryKey?: string;
  currentTicker?: string;
  onSelectTicker: (ticker: string) => void;
}

interface TrendingPopupContentProps {
  isLoading: boolean;
  error: Error | null;
  displayData: Array<{ symbol: string; name: string }>;
  selectedIndex: number;
  handleSelect: (ticker: string) => void;
  setSelectedIndex: (index: number) => void;
}

// --- Sub-Components (Rule 2.8, 2.23) ---
function TrendingPopupContent({
  isLoading,
  error,
  displayData,
  selectedIndex,
  handleSelect,
  setSelectedIndex
}: TrendingPopupContentProps) {
  const { t } = useTranslation();

  if (isLoading && !displayData.length) {
    return (
      <div className="p-4 flex justify-center text-on-surface-variant">
        <span className="material-symbols-outlined animate-spin text-2xl">progress_activity</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-3 text-xs text-error">
        {t('search.error_trending')}
      </div>
    );
  }

  if (!isLoading && displayData.length === 0) {
    return (
      <div className="p-3 text-xs text-on-surface-variant text-center">
        {t('search.empty_trending')}
      </div>
    );
  }

  return (
    <>
      {displayData.map((item, index) => (
        <SearchResultItem
          key={item.symbol}
          symbol={item.symbol}
          name={item.name}
          isSelected={index === selectedIndex}
          onSelect={() => handleSelect(item.symbol)}
          onHover={() => setSelectedIndex(index)}
        />
      ))}
    </>
  );
}

// --- Main Component ---
export function TrendingBadge({ 
  label, 
  value, 
  type, 
  queryKey, 
  currentTicker, 
  onSelectTicker 
}: TrendingBadgeProps) {
  const { t } = useTranslation();
  
  const {
    isOpen,
    selectedIndex,
    setSelectedIndex,
    containerRef,
    isLoading,
    error,
    displayData,
    handleToggle,
    handleSelect,
    handleKeyDown,
  } = useTrendingBadge({ type, queryKey, currentTicker, onSelectTicker });

  return (
    <div className="relative inline-block" ref={containerRef} onKeyDown={handleKeyDown}>
      <button 
        onClick={handleToggle}
        disabled={!queryKey}
        className={`px-3 py-1 bg-surface-container rounded-sm text-xs font-semibold tracking-wider text-on-surface-variant uppercase border border-outline-variant flex items-center gap-1 transition-colors hover:bg-surface-container-high focus:outline-none focus:ring-1 focus:ring-primary ${!queryKey ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}`}
      >
        <span className="opacity-70">{label}:</span> {value}
        {queryKey ? (
          <span className="material-symbols-outlined text-[14px] opacity-70">
            {isOpen ? 'expand_less' : 'expand_more'}
          </span>
        ) : null}
      </button>

      {isOpen ? (
        <div className="absolute top-full left-0 mt-1 w-72 bg-surface-container-high border border-outline-variant rounded-md shadow-lg z-50 overflow-hidden flex flex-col max-h-[400px]">
          <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex items-center justify-between">
            <span className="text-xs font-medium text-on-surface">{t('search.trending_in', { sector: value })}</span>
            {isLoading ? <span className="material-symbols-outlined text-[14px] animate-spin text-on-surface-variant">sync</span> : null}
          </div>
          
          <div className="overflow-y-auto">
            <TrendingPopupContent 
              isLoading={isLoading}
              error={error}
              displayData={displayData}
              selectedIndex={selectedIndex}
              handleSelect={handleSelect}
              setSelectedIndex={setSelectedIndex}
            />
          </div>
        </div>
      ) : null}
    </div>
  );
}
