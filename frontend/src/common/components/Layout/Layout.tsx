import React, { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
  onSearch: (ticker: string) => void;
  activeTicker?: string;
}

export function Layout({ children, onSearch, activeTicker }: LayoutProps) {
  const [searchTerm, setSearchTerm] = React.useState('MSFT');

  const handleSearch = () => {
    if (searchTerm.trim()) {
      onSearch(searchTerm.toUpperCase());
      setSearchTerm('');
    }
  };

  return (
    <div className="font-body-base text-body-base selection:bg-primary/30 min-h-screen flex flex-col">
      {/* TopAppBar */}
      <header className="bg-surface-dim dark:bg-surface-dim flex justify-between items-center w-full px-container h-10 z-50 fixed top-0 border-b border-outline-variant">
        <div className="flex items-center gap-4 h-full">
          <span className="font-header-sm text-header-sm font-bold text-primary dark:text-primary ml-4">Equity Valuation Engine</span>
          <div className="flex items-center bg-surface-container-high rounded border border-outline-variant px-2 h-7 ml-4">
            <span className="material-symbols-outlined text-[16px] text-outline mr-2">search</span>
            <input 
              className="bg-transparent border-none text-data-mono text-body-sm focus:ring-0 p-0 w-24 outline-none text-on-surface" 
              type="text" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button 
              onClick={handleSearch}
              className="bg-primary text-on-primary text-[10px] font-bold px-2 py-0.5 rounded ml-2 hover:opacity-90 active:opacity-80 transition-opacity"
            >
              ANALYSE
            </button>
          </div>
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
      <aside className="bg-surface-container-low dark:bg-surface-container-low fixed left-0 top-10 h-[calc(100vh-40px)] w-16 hover:w-64 transition-all duration-300 border-r border-outline-variant flex flex-col py-panel-gap z-40 group">
        <div className="px-4 py-2 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-primary-container flex items-center justify-center text-on-primary-container font-bold text-sm shrink-0">
              {activeTicker ? activeTicker[0] : 'T'}
            </div>
            <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 overflow-hidden whitespace-nowrap">
              <p className="font-header-sm text-header-sm font-bold text-on-surface">{activeTicker || 'TICKER'}</p>
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

      {/* Main Content Canvas */}
      <main className="ml-16 mt-10 p-panel-gap min-h-[calc(100vh-40px)] transition-all">
        {children}
      </main>
    </div>
  );
}
