import { type ReactNode } from 'react';
import { useIsFetching } from '@tanstack/react-query';
import { TopAppBar } from './TopAppBar';
import { SideNavBar } from './SideNavBar';

interface LayoutProps {
  children: ReactNode;
  onSearch: (ticker: string) => void;
  activeTicker?: string;
  hasError?: boolean;
  activeTab?: string;
  onTabChange?: (tab: string) => void;
}

export function Layout({ children, onSearch, activeTicker, hasError, activeTab, onTabChange }: LayoutProps) {
  const isFetching = useIsFetching({
    predicate: (query) => query.queryKey[0] !== 'search'
  });
  const isLoading = isFetching > 0;
  const shouldShowNav = Boolean(activeTicker && !isLoading && !hasError);

  return (
    <div className="font-body-base text-body-base selection:bg-primary/30 min-h-screen flex flex-col">
      <TopAppBar 
        onSearch={onSearch} 
        activeTicker={activeTicker} 
      />

      {shouldShowNav ? (
        <SideNavBar 
          activeTicker={activeTicker!} 
          activeTab={activeTab} 
          onTabChange={onTabChange} 
        />
      ) : null}

      <main className={`${shouldShowNav ? 'ml-16' : ''} mt-10 p-panel-gap min-h-[calc(100vh-40px)] transition-all`}>
        {children}
      </main>
    </div>
  );
}
