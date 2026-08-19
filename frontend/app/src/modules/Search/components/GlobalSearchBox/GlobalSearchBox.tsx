import { useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useSearchBox } from '@/modules/Search/hooks/useSearchBox';
import { SearchDropdown } from '@/modules/Search/components/SearchDropdown/SearchDropdown';
import { useClickOutside } from '@/common/hooks/useClickOutside';

interface GlobalSearchBoxProps {
  variant: 'header' | 'home';
}

export function GlobalSearchBox({ variant }: GlobalSearchBoxProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [isFocused, setIsFocused] = useState(false);
  
  const handleSearchCommit = (ticker: string) => {
    navigate(`/${ticker}`);
  };

  const {
    searchTerm,
    setSearchTerm,
    showHistory,
    setShowHistory,
    selectedIndex,
    setSelectedIndex,
    searchResults,
    filteredHistory,
    isSearchingAPI,
    handleKeyDown,
    clearHistory,
    handleSearch
  } = useSearchBox(handleSearchCommit);

  const containerRef = useRef<HTMLDivElement>(null);
  useClickOutside(containerRef, () => setShowHistory(false));

  const isHeader = variant === 'header';

  return (
    <div className={isHeader ? "relative" : "relative w-full max-w-2xl mx-auto"} ref={containerRef}>
      {isHeader ? (
        <>
          <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
          <input
            type="text"
            className="w-full bg-surface-container border border-outline-variant rounded-full py-2 pl-12 pr-4 text-sm text-on-surface placeholder:text-on-surface-variant focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
            placeholder={t('search.placeholder')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onFocus={() => { setIsFocused(true); setShowHistory(true); }}
            onBlur={() => { setIsFocused(false); }}
            onKeyDown={handleKeyDown}
          />
        </>
      ) : (
        <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="relative group w-full">
          <div className={`flex items-center px-6 py-4 bg-surface-container-high border ${isFocused ? 'border-primary ring-2 ring-primary/20' : 'border-outline-variant'} rounded-full shadow-lg transition-all`}>
            <span className="material-symbols-outlined text-on-surface-variant mr-4 text-2xl">search</span>
            <input
              type="text"
              className="w-full bg-transparent border-none outline-none text-on-surface placeholder:text-on-surface-variant text-lg pr-24"
              placeholder={t('search.placeholder')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onFocus={() => { setIsFocused(true); setShowHistory(true); }}
              onBlur={() => { setIsFocused(false); }}
              onKeyDown={handleKeyDown}
            />
            <button
              type="button"
              onClick={() => handleSearch()}
              disabled={!searchTerm.trim()}
              className="absolute inset-y-2 right-2 px-6 bg-primary text-on-primary font-bold rounded-full hover:opacity-90 active:opacity-80 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {t('search.analyze')}
            </button>
          </div>
        </form>
      )}

      <SearchDropdown 
        show={showHistory} 
        searchTerm={searchTerm} 
        filteredHistory={filteredHistory}
        searchResults={searchResults}
        isFetching={isSearchingAPI}
        selectedIndex={selectedIndex}
        onSelect={(t, n) => {
          handleSearch(t, n);
        }}
        onHover={setSelectedIndex}
        onClearHistory={clearHistory}
        className={isHeader ? "absolute top-10 left-0 right-0 w-full" : "absolute top-full left-0 right-0 mt-2"}
      />
    </div>
  );
}
