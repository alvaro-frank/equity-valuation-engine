import { useTranslation } from 'react-i18next';

import { useSearchBox } from '@/common/hooks/useSearchBox';
import { SearchResultItem } from '@/common/components/SearchResultItem';
import { SearchHistoryItem } from '@/common/components/SearchHistoryItem';
import { ThemeToggle } from '@/common/components/ThemeToggle/ThemeToggle';

// --- Sub-Components (Rule 2.12, 2.23, 2.31) ---

function SearchResultsList({ searchResults, selectedIndex, handleSearch, setSelectedIndex, isSearchingAPI }: { searchResults: unknown[]; selectedIndex: number; handleSearch: (ticker: string) => void; setSelectedIndex: (idx: number) => void; isSearchingAPI: boolean }) {
  if (!searchResults || searchResults.length === 0) {
    return (
      <div className="px-3 py-3 text-xs text-on-surface-variant flex items-center gap-2">
        {isSearchingAPI ? (
          <>
            <span className="material-symbols-outlined animate-spin text-[14px]">progress_activity</span>
            Searching...
          </>
        ) : (
          <>
            <span className="material-symbols-outlined text-[14px]">search_off</span>
            No results
          </>
        )}
      </div>
    );
  }

  return (
    <>
      {searchResults.map((item: { symbol: string; name: string; exchange?: string }, index: number) => (
        <SearchResultItem
          key={item.symbol}
          symbol={item.symbol}
          name={item.name}
          exchange={item.exchange}
          isSelected={index === selectedIndex}
          onSelect={() => handleSearch(item.symbol)}
          onHover={() => setSelectedIndex(index)}
        />
      ))}
    </>
  );
}

function SearchDropdown({
  searchTerm,
  filteredHistory,
  searchResults,
  selectedIndex,
  setSelectedIndex,
  isSearchingAPI,
  handleSearch,
  clearHistory,
  t
}: { searchTerm: string; filteredHistory: unknown[]; searchResults: unknown[]; selectedIndex: number; setSelectedIndex: (idx: number) => void; isSearchingAPI: boolean; handleSearch: (ticker: string) => void; clearHistory: () => void; t: (key: string) => string }) {
  const hasSearchTerm = searchTerm.trim().length > 0;

  if (hasSearchTerm) {
    return (
      <div className="absolute top-8 left-4 min-w-[280px] bg-surface-container-high border border-outline-variant rounded shadow-lg overflow-hidden z-50">
        <div className="px-3 py-1.5 text-[10px] font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant uppercase tracking-wider flex justify-between items-center">
          <span>SEARCH RESULTS</span>
          {isSearchingAPI ? <span className="material-symbols-outlined animate-spin text-[12px]">refresh</span> : null}
        </div>
        <div className="flex flex-col max-h-[300px] overflow-y-auto">
          <SearchResultsList 
            searchResults={searchResults}
            selectedIndex={selectedIndex}
            handleSearch={handleSearch}
            setSelectedIndex={setSelectedIndex}
            isSearchingAPI={isSearchingAPI}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="absolute top-8 left-4 min-w-[280px] bg-surface-container-high border border-outline-variant rounded shadow-lg overflow-hidden z-50">
      <div className="px-3 py-1.5 text-[10px] font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant flex justify-between items-center">
        <span>{t('search.recent_searches')}</span>
        <button 
          onMouseDown={(e) => {
            e.preventDefault();
            e.stopPropagation();
            clearHistory();
          }}
          className="text-error hover:text-error/80 cursor-pointer transition-colors"
        >
          {t('search.clear')}
        </button>
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        {filteredHistory.map((item: { ticker: string; name?: string }, index: number) => (
          <SearchHistoryItem
            key={item.ticker}
            ticker={item.ticker}
            name={item.name}
            isSelected={index === selectedIndex}
            onSelect={() => handleSearch(item.ticker)}
            onHover={() => setSelectedIndex(index)}
          />
        ))}
      </div>
    </div>
  );
}

// --- Main Component ---

interface TopAppBarProps {
  onSearch: (ticker: string) => void;
  activeTicker?: string;
}

export function TopAppBar({ onSearch, activeTicker }: TopAppBarProps) {
  const { t, i18n } = useTranslation();
  const {
    searchTerm,
    setSearchTerm,
    showHistory,
    selectedIndex,
    setSelectedIndex,
    searchResults,
    filteredHistory,
    isSearchingAPI,
    isSearchDisabled,
    handleSearch,
    handleKeyDown,
    handleFocus,
    handleBlur,
    clearHistory
  } = useSearchBox(onSearch);

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === 'pt' ? 'en' : 'pt');
  };

  const shouldShowDropdown = showHistory && (searchTerm.trim().length > 0 || filteredHistory.length > 0);

  return (
    <header className="bg-surface-dim dark:bg-surface-dim flex justify-between items-center w-full px-container h-10 z-50 fixed top-0 border-b border-outline-variant">
      <div className="flex items-center gap-4 h-full">
        <span className="font-header-sm text-header-sm font-bold text-primary dark:text-primary ml-4">Equity Valuation Engine</span>
        {activeTicker ? (
          <div className="relative">
            <div className="flex items-center bg-surface-container-high rounded border border-outline-variant px-2 h-7 ml-4">
              <span className="material-symbols-outlined text-[16px] text-outline mr-2">search</span>
              <input 
                className="bg-transparent border-none text-data-mono text-body-sm focus:ring-0 p-0 w-24 outline-none text-on-surface" 
                type="text" 
                placeholder={t('search.placeholder')}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={handleKeyDown}
                onFocus={handleFocus}
                onBlur={handleBlur}
              />
              <button 
                onClick={() => handleSearch()}
                disabled={isSearchDisabled}
                className="bg-primary text-on-primary text-[10px] font-bold px-2 py-0.5 rounded ml-2 hover:opacity-90 active:opacity-80 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {t('search.analyze')}
              </button>
            </div>

            {shouldShowDropdown ? (
              <SearchDropdown 
                searchTerm={searchTerm}
                filteredHistory={filteredHistory}
                searchResults={searchResults}
                selectedIndex={selectedIndex}
                setSelectedIndex={setSelectedIndex}
                isSearchingAPI={isSearchingAPI}
                handleSearch={handleSearch}
                clearHistory={clearHistory}
                t={t}
              />
            ) : null}
          </div>
        ) : null}
      </div>
      <div className="flex items-center gap-4">
        <button 
          onClick={toggleLanguage}
          className="flex items-center justify-center w-8 h-8 rounded hover:bg-surface-container-highest transition-colors font-bold text-xs"
          title="Toggle Language"
        >
          {i18n.language === 'pt' ? 'PT' : 'EN'}
        </button>
        <div className="flex gap-2 items-center">
          <ThemeToggle className="w-8 h-8 !p-1 !rounded" />
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">notifications</span>
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">history</span>
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">settings</span>
        </div>
        <div className="w-6 h-6 rounded-full overflow-hidden border border-outline-variant flex items-center justify-center bg-surface-container-high text-[10px] font-bold text-on-surface">
          AF
        </div>
      </div>
    </header>
  );
}
