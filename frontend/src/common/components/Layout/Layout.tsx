import { type ReactNode } from 'react';
import { useIsFetching } from '@tanstack/react-query';
import { CompanyLogo } from '@/common/components/CompanyLogo';
import { SearchHistoryItem } from '@/common/components/SearchHistoryItem';
import { SearchResultItem } from '@/common/components/SearchResultItem';
import { useSearchBox } from '@/common/hooks/useSearchBox';

interface LayoutProps {
  children: ReactNode;
  onSearch: (ticker: string) => void;
  activeTicker?: string;
  hasError?: boolean;
}

export function Layout({ children, onSearch, activeTicker, hasError }: LayoutProps) {
  const isFetching = useIsFetching({
    predicate: (query) => query.queryKey[0] !== 'search'
  });
  const isLoading = isFetching > 0;
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

  const activeCompany = filteredHistory.find(item => item.ticker === activeTicker);
  const activeName = activeCompany?.name;

  return (
    <div className="font-body-base text-body-base selection:bg-primary/30 min-h-screen flex flex-col">
      {/* TopAppBar */}
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
                      ANALYSE
                    </button>
                  </div>

                  {showHistory && (searchTerm.trim().length > 0 || filteredHistory.length > 0) ? (
                    <div className="absolute top-8 left-4 min-w-[280px] bg-surface-container-high border border-outline-variant rounded shadow-lg overflow-hidden z-50">
                      {searchTerm.trim().length > 0 ? (
                        // Search Results rendering
                        <>
                          <div className="px-3 py-1.5 text-[10px] font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant uppercase tracking-wider flex justify-between items-center">
                            <span>SEARCH RESULTS</span>
                            {isSearchingAPI && <span className="material-symbols-outlined animate-spin text-[12px]">refresh</span>}
                          </div>
                          <div className="flex flex-col max-h-[300px] overflow-y-auto">
                            {searchResults && searchResults.length > 0 ? (
                              searchResults.map((item, index) => (
                                <SearchResultItem
                                  key={item.symbol}
                                  symbol={item.symbol}
                                  name={item.name}
                                  exchange={item.exchange}
                                  isSelected={index === selectedIndex}
                                  onSelect={() => handleSearch(item.symbol)}
                                  onHover={() => setSelectedIndex(index)}
                                />
                              ))
                            ) : (
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
                            )}
                          </div>
                        </>
                      ) : (
                        // Recent Searches rendering
                        <>
                          <div className="px-3 py-1.5 text-[10px] font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant flex justify-between items-center">
                            <span>RECENT SEARCHES</span>
                            <button 
                              onMouseDown={(e) => {
                                e.preventDefault();
                                e.stopPropagation();
                                clearHistory();
                              }}
                              className="text-error hover:text-error/80 cursor-pointer transition-colors"
                            >
                              Clear
                            </button>
                          </div>
                          <div className="flex flex-col max-h-[300px] overflow-y-auto">
                            {filteredHistory.map((item, index) => (
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
                        </>
                      )}
                    </div>
                  ) : null}
                </div>
              ) : null}
        </div>
        <div className="flex items-center gap-4">
          <div className="flex gap-2">
            <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">notifications</span>
            <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">history</span>
            <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">settings</span>
          </div>
          <div className="w-6 h-6 rounded-full overflow-hidden border border-outline-variant">
            <img alt="Analyst Profile" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCWYetn8XG4h05759AyzSf-sqREeSwowYNL4W7UOMp0iVAmMZIH3O7FKNMaczfaGG8wyQSz55qbM5oNwcfmHL_jOgGqh8kXRGidp2_iRQEfrX5fpmJPn8JjDVyz9Koh-yA89_MFnAhpsawhIbg4pcdxSDZCoioQMIHDgB123C1ZfVO7IEJWzqmbPvcKgkC2DHYjqN14yEpqqSIIaMEVKpWqzkok_mSttev_gKfpXYtdEe02Rws_cVJ-WbKdSSUAHWsNUn9VE-VRH2Q" />
          </div>
        </div>
      </header>

      {/* SideNavBar */}
      {activeTicker && !isLoading && !hasError ? (
        <aside className="bg-surface-container-low dark:bg-surface-container-low fixed left-0 top-10 h-[calc(100vh-40px)] w-16 hover:w-64 transition-all duration-300 border-r border-outline-variant flex flex-col py-panel-gap z-40 group">
          <div className="px-4 py-2 mb-4">
            <div className="flex items-center gap-3">
              <CompanyLogo ticker={activeTicker} />
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 overflow-hidden whitespace-nowrap flex flex-col justify-center">
                <p className="font-header-sm text-header-sm font-bold text-on-surface leading-tight">{activeTicker || 'TICKER'}</p>
                {activeName && <p className="text-on-surface-variant text-[11px] font-medium truncate max-w-[140px] mt-0.5">{activeName}</p>}
              </div>
            </div>
          </div>
          <nav className="flex-1 px-3 space-y-1">
            {[
              { icon: 'dashboard', label: 'SUMMARY', active: true },
              { icon: 'account_balance', label: 'FINANCIALS' },
              { icon: 'calculate', label: 'VALUATION' },
              { icon: 'analytics', label: 'COMPARABLES' },
              { icon: 'description', label: 'FILINGS' }
            ].map(item => (
              <button 
                key={item.label}
                className={`${item.active ? 'bg-secondary-container text-on-secondary-container border-r-2 border-primary' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'} flex items-center w-full h-10 px-2 rounded-sm group/item transition-colors`}
              >
                <span className="material-symbols-outlined">{item.icon}</span>
                <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{item.label}</span>
              </button>
            ))}
          </nav>
          <div className="px-3 space-y-1 mt-auto border-t border-outline-variant pt-4">
            {[
              { icon: 'help', label: 'SUPPORT' },
              { icon: 'code', label: 'API' }
            ].map(item => (
              <button key={item.label} className="text-on-surface-variant hover:text-on-surface w-full hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm transition-colors">
                <span className="material-symbols-outlined">{item.icon}</span>
                <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{item.label}</span>
              </button>
            ))}
          </div>
        </aside>
      ) : null}

      {/* Main Content Canvas */}
      <main className={`${activeTicker && !hasError ? 'ml-16' : ''} mt-10 p-panel-gap min-h-[calc(100vh-40px)] transition-all`}>
        {children}
      </main>
    </div>
  );
}
