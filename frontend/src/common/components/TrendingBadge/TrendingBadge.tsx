import { useState, useRef, useEffect } from 'react';
import { useTrendingTickers } from '@/common/hooks/useTrendingTickers';
import { SearchResultItem } from '@/common/components/SearchResultItem';

interface TrendingBadgeProps {
  label: string;
  value: string;
  type: 'sector' | 'industry';
  queryKey?: string;
  currentTicker?: string;
  onSelectTicker: (ticker: string) => void;
}

export function TrendingBadge({ label, value, type, queryKey, currentTicker, onSelectTicker }: TrendingBadgeProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const { data, isLoading, error } = useTrendingTickers(isOpen ? type : null, queryKey || null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = () => {
    if (!queryKey) return;
    setIsOpen(!isOpen);
  };

  const handleSelect = (ticker: string) => {
    setIsOpen(false);
    onSelectTicker(ticker);
  };

  return (
    <div className="relative inline-block" ref={containerRef}>
      <button 
        onClick={handleToggle}
        disabled={!queryKey}
        className={`px-3 py-1 bg-surface-container rounded-sm text-xs font-semibold tracking-wider text-on-surface-variant uppercase border border-outline-variant flex items-center gap-1 transition-colors hover:bg-surface-container-high focus:outline-none focus:ring-1 focus:ring-primary ${!queryKey ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'}`}
      >
        <span className="opacity-70">{label}:</span> {value}
        {queryKey && (
          <span className="material-symbols-outlined text-[14px] opacity-70">
            {isOpen ? 'expand_less' : 'expand_more'}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-1 w-72 bg-surface-container-high border border-outline-variant rounded-md shadow-lg z-50 overflow-hidden flex flex-col max-h-[400px]">
          <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex items-center justify-between">
            <span className="text-xs font-medium text-on-surface">Trending in {value}</span>
            {isLoading && <span className="material-symbols-outlined text-[14px] animate-spin text-on-surface-variant">sync</span>}
          </div>
          
          <div className="overflow-y-auto">
            {isLoading && !data.length && (
              <div className="p-4 flex justify-center text-on-surface-variant">
                <span className="material-symbols-outlined animate-spin text-2xl">progress_activity</span>
              </div>
            )}
            
            {error && (
              <div className="p-3 text-xs text-error">
                Failed to load trending companies.
              </div>
            )}

            {!isLoading && !error && data.length === 0 && (
              <div className="p-3 text-xs text-on-surface-variant text-center">
                No trending data found.
              </div>
            )}

            {data
              .filter((item) => item.symbol !== currentTicker)
              .map((item) => (
              <SearchResultItem
                key={item.symbol}
                symbol={item.symbol}
                name={item.name}
                isSelected={false}
                onSelect={() => handleSelect(item.symbol)}
                onHover={() => {}}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
