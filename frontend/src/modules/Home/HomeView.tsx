import { useTranslation } from 'react-i18next';
import { useSearchBox } from '@/common/hooks/useSearchBox';

import { HomeHero } from './components/HomeHero';
import { TrendingTickers } from './components/TrendingTickers';
import { SearchDropdown } from './components/SearchDropdown';

interface HomeViewProps {
  onSearch: (ticker: string) => void;
}

export function HomeView({ onSearch }: HomeViewProps) {
  const {
    searchTerm,
    setSearchTerm,
    showHistory,
    selectedIndex,
    setSelectedIndex,
    searchResults,
    filteredHistory,
    isSearchingAPI: isFetching,
    isSearchDisabled,
    handleSearch,
    handleKeyDown,
    handleFocus,
    handleBlur,
    clearHistory
  } = useSearchBox(onSearch);

  const { t } = useTranslation();

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] max-w-2xl mx-auto w-full px-4 animate-fade-in">
      <HomeHero />

      {/* Main Search Bar */}
      <form onSubmit={(e) => { e.preventDefault(); handleSearch(searchTerm); }} className="w-full relative group z-50">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <span className="material-symbols-outlined text-outline group-focus-within:text-primary transition-colors text-2xl">
            search
          </span>
        </div>
        <input
          type="text"
          className="w-full bg-surface-container-high border border-outline-variant rounded-full py-4 pl-12 pr-24 text-on-surface text-body-lg focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-lg transition-all"
          placeholder={t('search.placeholder')}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={handleFocus}
          onBlur={handleBlur}
        />
        <button
          type="button"
          onClick={() => handleSearch()}
          disabled={isSearchDisabled}
          className="absolute inset-y-2 right-2 px-6 bg-primary text-on-primary font-bold rounded-full hover:opacity-90 active:opacity-80 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {t('search.analyze')}
        </button>

        <SearchDropdown
          show={showHistory}
          searchTerm={searchTerm}
          isFetching={isFetching}
          searchResults={searchResults}
          filteredHistory={filteredHistory}
          selectedIndex={selectedIndex}
          onSelect={(symbol, name) => handleSearch(symbol, name)}
          onHover={setSelectedIndex}
          onClearHistory={clearHistory}
        />
      </form>

      <TrendingTickers onSelect={(symbol, name) => handleSearch(symbol, name)} />
    </div>
  );
}
