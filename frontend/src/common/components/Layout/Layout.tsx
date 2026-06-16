import { type ReactNode } from 'react';
import { Outlet, useParams } from 'react-router-dom';
import { TopAppBar } from './TopAppBar';
import { SideNavBar } from './SideNavBar';
import { useTickerValidation } from '@/common/api/hooks/useTickerValidation';

interface LayoutProps {
  children?: ReactNode;
  headerSearchComponent?: ReactNode;
}

export function Layout({ children, headerSearchComponent }: LayoutProps) {
  const { ticker: activeTicker } = useParams<{ ticker?: string }>();

  const { data, isLoading } = useTickerValidation(activeTicker ?? '');

  // Show the sidebar only when the ticker is confirmed valid by the API
  const shouldShowNav = Boolean(activeTicker && !isLoading && data?.valid);

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
