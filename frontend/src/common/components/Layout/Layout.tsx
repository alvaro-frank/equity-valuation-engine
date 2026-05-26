import React, { ReactNode } from 'react';
import { CompanyLogo } from '../CompanyLogo';
import { useSearchHistory } from '../../hooks/useSearchHistory';

interface LayoutProps {
  children: ReactNode;
  onSearch: (ticker: string) => void;
  activeTicker?: string;
}

export function Layout({ children, onSearch, activeTicker }: LayoutProps) {
  const [searchTerm, setSearchTerm] = React.useState('');
  const { history: searchHistory, addSearch, clearHistory } = useSearchHistory();
  const [showHistory, setShowHistory] = React.useState(false);
  const [selectedIndex, setSelectedIndex] = React.useState(-1);

  const activeCompany = searchHistory.find(item => item.ticker === activeTicker);
  const activeName = activeCompany?.name;

  React.useEffect(() => {
    if (!showHistory) {
      setSelectedIndex(-1);
    }
  }, [showHistory]);

  const handleSearch = (termToSearch: string = searchTerm) => {
    if (termToSearch.trim()) {
      const upperTerm = termToSearch.toUpperCase();
      onSearch(upperTerm);
      addSearch(upperTerm);
      setSearchTerm('');
      setShowHistory(false);
    }
  };

  return (
    <div className="font-body-base text-body-base selection:bg-primary/30 min-h-screen flex flex-col">
      {/* TopAppBar */}
      <header className="bg-surface-dim dark:bg-surface-dim flex justify-between items-center w-full px-container h-10 z-50 fixed top-0 border-b border-outline-variant">
        <div className="flex items-center gap-4 h-full">
          <span className="font-header-sm text-header-sm font-bold text-primary dark:text-primary ml-4">Equity Valuation Engine</span>
          {activeTicker && (
            <div className="relative">
              <div className="flex items-center bg-surface-container-high rounded border border-outline-variant px-2 h-7 ml-4">
                <span className="material-symbols-outlined text-[16px] text-outline mr-2">search</span>
                <input 
                  className="bg-transparent border-none text-data-mono text-body-sm focus:ring-0 p-0 w-24 outline-none text-on-surface" 
                  type="text" 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'ArrowDown') {
                      e.preventDefault();
                      setSelectedIndex(prev => (prev < searchHistory.length - 1 ? prev + 1 : prev));
                    } else if (e.key === 'ArrowUp') {
                      e.preventDefault();
                      setSelectedIndex(prev => (prev > -1 ? prev - 1 : -1));
                    } else if (e.key === 'Enter') {
                      e.preventDefault();
                      if (selectedIndex >= 0 && selectedIndex < searchHistory.length) {
                        handleSearch(searchHistory[selectedIndex].ticker);
                      } else {
                        handleSearch();
                      }
                    } else if (e.key === 'Escape') {
                      setShowHistory(false);
                      setSelectedIndex(-1);
                    }
                  }}
                  onFocus={() => setShowHistory(true)}
                  onBlur={() => setTimeout(() => setShowHistory(false), 200)}
                />
                <button 
                  onClick={() => handleSearch()}
                  className="bg-primary text-on-primary text-[10px] font-bold px-2 py-0.5 rounded ml-2 hover:opacity-90 active:opacity-80 transition-opacity"
                >
                  ANALYSE
                </button>
              </div>

              {showHistory && searchHistory.length > 0 && (
                <div className="absolute top-8 left-4 min-w-[200px] bg-surface-container-high border border-outline-variant rounded shadow-lg overflow-hidden z-50">
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
                  <div className="flex flex-col">
                    {searchHistory.map((item, index) => (
                      <div 
                        key={item.ticker}
                        className={`px-3 py-2 text-sm text-on-surface cursor-pointer flex items-center transition-colors ${index === selectedIndex ? 'bg-surface-container-highest' : 'hover:bg-surface-container-highest'}`}
                        onMouseDown={(e) => {
                          e.preventDefault();
                          handleSearch(item.ticker);
                        }}
                        onMouseEnter={() => setSelectedIndex(index)}
                      >
                        <span className="material-symbols-outlined text-[14px] text-outline mr-2">history</span>
                        <div className="flex items-center gap-2">
                          <CompanyLogo ticker={item.ticker} className="w-5 h-5 text-[10px]" fallbackLetter={item.ticker[0]} />
                          <span className="font-data-mono">{item.ticker}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
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
      {activeTicker && (
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
            <a className="bg-secondary-container text-on-secondary-container border-r-2 border-primary flex items-center h-10 px-2 rounded-sm group/item" href="#">
              <span className="material-symbols-outlined">dashboard</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">SUMMARY</span>
            </a>
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm group/item transition-colors" href="#">
              <span className="material-symbols-outlined">account_balance</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">FINANCIALS</span>
            </a>
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm group/item transition-colors" href="#">
              <span className="material-symbols-outlined">calculate</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">VALUATION</span>
            </a>
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm group/item transition-colors" href="#">
              <span className="material-symbols-outlined">analytics</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">COMPARABLES</span>
            </a>
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm group/item transition-colors" href="#">
              <span className="material-symbols-outlined">description</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">FILINGS</span>
            </a>
          </nav>
          <div className="px-3 space-y-1 mt-auto border-t border-outline-variant pt-4">
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm transition-colors" href="#">
              <span className="material-symbols-outlined">help</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">SUPPORT</span>
            </a>
            <a className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm transition-colors" href="#">
              <span className="material-symbols-outlined">code</span>
              <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">API</span>
            </a>
          </div>
        </aside>
      )}

      {/* Main Content Canvas */}
      <main className={`${activeTicker ? 'ml-16' : ''} mt-10 p-panel-gap min-h-[calc(100vh-40px)] transition-all`}>
        {children}
      </main>
    </div>
  );
}
