import React, { useState } from 'react';
import { CompanyLogo } from '../../../common/components/CompanyLogo';
import { useSearchHistory } from '../../../common/hooks/useSearchHistory';

interface WelcomeStateProps {
  onSearch: (ticker: string) => void;
}

export function WelcomeState({ onSearch }: WelcomeStateProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const { history: searchHistory, addSearch, clearHistory } = useSearchHistory();
  const [showHistory, setShowHistory] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  React.useEffect(() => {
    if (!showHistory) {
      setSelectedIndex(-1);
    }
  }, [showHistory]);

  const handleSearch = (e?: React.FormEvent, termToSearch: string = searchTerm, nameToSearch?: string) => {
    if (e) e.preventDefault();
    if (termToSearch.trim()) {
      const upperTerm = termToSearch.trim().toUpperCase();
      addSearch(upperTerm, nameToSearch);
      onSearch(upperTerm);
    }
  };

  const suggestedTickers = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'MSFT', name: 'Microsoft Corp.' },
    { symbol: 'NVDA', name: 'NVIDIA Corp.' },
    { symbol: 'TSLA', name: 'Tesla Inc.' },
    { symbol: 'AMZN', name: 'Amazon.com' },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] max-w-2xl mx-auto w-full px-4 animate-fade-in">
      
      {/* Brand & Logo */}
      <div className="flex items-center gap-3 mb-8">
        <span className="material-symbols-outlined text-5xl text-primary drop-shadow-[0_0_15px_rgba(var(--color-primary),0.3)]">
          monitoring
        </span>
        <h1 className="font-display-lg text-4xl font-bold tracking-tight text-on-surface">
          Equity Valuation Engine
        </h1>
      </div>

      <p className="text-on-surface-variant text-body-lg mb-8 text-center max-w-lg">
        Professional-grade fundamental analysis and automated valuation modeling for public equities.
      </p>

      {/* Main Search Bar */}
      <form onSubmit={handleSearch} className="w-full relative group z-50">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <span className="material-symbols-outlined text-outline group-focus-within:text-primary transition-colors text-2xl">
            search
          </span>
        </div>
        <input
          type="text"
          className="w-full bg-surface-container-high border border-outline-variant rounded-full py-4 pl-12 pr-24 text-on-surface text-body-lg focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary shadow-lg transition-all"
          placeholder="Search for a ticker (e.g. MSFT)"
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
                handleSearch(undefined, searchHistory[selectedIndex].ticker, searchHistory[selectedIndex].name);
              } else {
                handleSearch(e);
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
          type="button"
          onClick={() => handleSearch()}
          disabled={!searchTerm.trim()}
          className="absolute inset-y-2 right-2 px-6 bg-primary text-on-primary font-bold rounded-full hover:opacity-90 active:opacity-80 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ANALYSE
        </button>

        {/* History Dropdown */}
        {showHistory && searchHistory.length > 0 && (
          <div className="absolute top-[110%] left-0 w-full bg-surface-container-high border border-outline-variant rounded-xl shadow-2xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
            <div className="px-4 py-2 text-xs font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant flex justify-between items-center">
              <span>RECENT SEARCHES</span>
              <button 
                type="button"
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
                  className={`px-4 py-3 text-base text-on-surface cursor-pointer flex items-center transition-colors ${index === selectedIndex ? 'bg-surface-container-highest' : 'hover:bg-surface-container-highest'}`}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    handleSearch(undefined, item.ticker, item.name);
                  }}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <span className="material-symbols-outlined text-[18px] text-outline mr-3">history</span>
                  <div className="flex items-center gap-2">
                    <CompanyLogo ticker={item.ticker} className="w-6 h-6 text-xs" fallbackLetter={item.ticker[0]} />
                    <span className="font-data-mono font-medium">{item.ticker}</span>
                    {item.name && <span className="text-on-surface-variant text-sm ml-1">- {item.name}</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </form>

      {/* Suggested Tickers */}
      <div className="mt-12 w-full">
        <p className="text-on-surface-variant font-label-caps text-label-caps mb-4 text-center">
          TRENDING TICKERS
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {suggestedTickers.map((ticker) => (
            <button
              key={ticker.symbol}
              onClick={() => handleSearch(undefined, ticker.symbol, ticker.name)}
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
    </div>
  );
}
