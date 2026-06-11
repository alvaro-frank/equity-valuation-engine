import { useTranslation } from 'react-i18next';
import { SearchHistoryItem } from '@/common/components/SearchHistoryItem';
import { SearchResultItem } from '@/common/components/SearchResultItem';

interface SearchDropdownProps {
  show: boolean;
  searchTerm: string;
  isFetching: boolean;
  searchResults: Array<{ symbol: string; name: string; exchange: string }> | undefined;
  filteredHistory: Array<{ ticker: string; name?: string }>;
  selectedIndex: number;
  onSelect: (ticker: string, name?: string) => void;
  onHover: (index: number) => void;
  onClearHistory: () => void;
}

// --- Sub-Components (Rule 2.23, 2.8, 2.9, 2.12) ---

function LoadingState() {
  return (
    <div className="px-4 py-4 text-sm text-on-surface-variant flex items-center gap-2">
      <span className="material-symbols-outlined animate-spin text-[16px]">progress_activity</span>
      Searching tickers...
    </div>
  );
}

function EmptyState({ searchTerm }: { searchTerm: string }) {
  return (
    <div className="px-4 py-4 text-sm text-on-surface-variant flex items-center gap-2">
      <span className="material-symbols-outlined text-[16px]">search_off</span>
      No tickers found matching "{searchTerm}"
    </div>
  );
}

function SearchResultsList(props: SearchDropdownProps) {
  const { searchResults, isFetching, searchTerm, selectedIndex, onSelect, onHover } = props;
  
  if (isFetching && (!searchResults || searchResults.length === 0)) {
    return <LoadingState />;
  }

  if (!searchResults || searchResults.length === 0) {
    return <EmptyState searchTerm={searchTerm} />;
  }

  return (
    <>
      {searchResults.map((item, index) => (
        <SearchResultItem
          key={item.symbol}
          symbol={item.symbol}
          name={item.name}
          exchange={item.exchange}
          isSelected={index === selectedIndex}
          onSelect={() => onSelect(item.symbol, item.name)}
          onHover={() => onHover(index)}
          className="px-4 py-3"
        />
      ))}
    </>
  );
}

function SearchResultsSection(props: SearchDropdownProps) {
  return (
    <>
      <div className="px-4 py-2 text-xs font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant uppercase tracking-wider flex justify-between items-center">
        <span>SEARCH RESULTS</span>
        {props.isFetching ? <span className="material-symbols-outlined animate-spin text-[14px]">refresh</span> : null}
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        <SearchResultsList {...props} />
      </div>
    </>
  );
}

function RecentSearchesSection(props: SearchDropdownProps) {
  const { t } = useTranslation();
  return (
    <>
      <div className="px-4 py-2 text-xs font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant flex justify-between items-center">
        <span>{t('search.recent_searches')}</span>
        <button 
          type="button"
          onMouseDown={(e) => {
            e.preventDefault();
            e.stopPropagation();
            props.onClearHistory();
          }}
          className="text-error hover:text-error/80 cursor-pointer transition-colors"
        >
          {t('search.clear')}
        </button>
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        {props.filteredHistory.map((item, index) => (
          <SearchHistoryItem
            key={item.ticker}
            ticker={item.ticker}
            name={item.name}
            isSelected={index === props.selectedIndex}
            onSelect={() => props.onSelect(item.ticker, item.name)}
            onHover={() => props.onHover(index)}
            className="px-4 py-3 text-base"
          />
        ))}
      </div>
    </>
  );
}

// --- Main Component ---

export function SearchDropdown(props: SearchDropdownProps) {
  const hasSearchTerm = props.searchTerm.trim().length > 0;
  
  if (!props.show) return null;
  if (!hasSearchTerm && props.filteredHistory.length === 0) return null;

  return (
    <div className="absolute top-[110%] left-0 w-full bg-surface-container-high border border-outline-variant rounded-xl shadow-2xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
      {hasSearchTerm ? (
        <SearchResultsSection {...props} />
      ) : (
        <RecentSearchesSection {...props} />
      )}
    </div>
  );
}
