import { type ReactNode } from 'react';
import { useIsFetching } from '@tanstack/react-query';
import { Outlet, useParams } from 'react-router-dom';
import { TopAppBar } from './TopAppBar';
import { SideNavBar } from './SideNavBar';

interface LayoutProps {
  children?: ReactNode;
  headerSearchComponent?: ReactNode;
}

export function Layout({ children, headerSearchComponent }: LayoutProps) {
  const { ticker: activeTicker } = useParams<{ ticker?: string }>();

  const isFetchingNewTicker = useIsFetching({
    predicate: (query) => 
      query.queryKey[0] === 'valuation' && 
      query.queryKey[1] === 'validate' && 
      query.queryKey[2] === activeTicker && 
      query.state.data === undefined
  });
  const isLoading = isFetchingNewTicker > 0;
  const shouldShowNav = Boolean(activeTicker && !isLoading);

  return (
    <div className="font-body-base text-body-base selection:bg-primary/30 min-h-screen flex flex-col">
      <TopAppBar 
        searchComponent={headerSearchComponent}
      />

      {shouldShowNav ? (
        <SideNavBar 
          activeTicker={activeTicker!} 
        />
      ) : null}

      <main className={`${shouldShowNav ? 'ml-16' : ''} flex-1 p-panel-gap transition-all`}>
        {children || <Outlet />}
      </main>
    </div>
  );
}
