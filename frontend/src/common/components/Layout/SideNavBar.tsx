import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';
import { CompanyLogo } from '@/common/components/CompanyLogo';
import { useSearchHistory } from '@/modules/Search/hooks/useSearchHistory';

interface SideNavBarProps {
  activeTicker: string;
}

export function SideNavBar({ activeTicker }: SideNavBarProps) {
  const { t } = useTranslation();
  const { history } = useSearchHistory();
  
  const activeCompany = history.find(item => item.ticker === activeTicker);
  const activeName = activeCompany?.name;

  return (
    <aside className="bg-surface-container-low dark:bg-surface-container-low fixed left-0 top-16 h-[calc(100vh-64px)] w-16 hover:w-64 transition-all duration-300 border-r border-outline-variant flex flex-col py-panel-gap z-40 group">
      <div className="px-4 py-2 mb-4">
        <div className="flex items-center gap-3">
          <CompanyLogo ticker={activeTicker} />
          <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 overflow-hidden whitespace-nowrap flex flex-col justify-center">
            <p className="font-header-sm text-header-sm font-bold text-on-surface leading-tight">{activeTicker || 'TICKER'}</p>
            {activeName ? <p className="text-on-surface-variant text-[11px] font-medium truncate max-w-[140px] mt-0.5">{activeName}</p> : null}
          </div>
        </div>
      </div>
      <nav className="flex-1 px-3 space-y-1">
        {[
          { icon: 'dashboard', label: t('nav.summary'), id: 'summary' },
          { icon: 'account_balance', label: t('nav.financials'), id: 'financials' },
          { icon: 'history_edu', label: t('nav.thesis'), id: 'thesis' },
          { icon: 'calculate', label: t('nav.valuation'), id: 'valuation' },
          { icon: 'analytics', label: t('nav.sector'), id: 'sector' },
          { icon: 'description', label: t('nav.filings'), id: 'filings' }
        ].map(item => (
          <NavLink 
            key={item.id}
            to={`/${activeTicker}/${item.id}`}
            className={({ isActive }) => 
              `${isActive ? 'bg-secondary-container text-on-secondary-container border-r-2 border-primary' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high'} flex items-center w-full h-10 px-2 rounded-sm group/item transition-colors`
            }
          >
            <span className="material-symbols-outlined">{item.icon}</span>
            <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="px-3 space-y-1 mt-auto border-t border-outline-variant pt-4">
        {[
          { icon: 'help', label: t('nav.support'), id: 'SUPPORT' },
          { icon: 'code', label: t('nav.api'), id: 'API' }
        ].map(item => (
          <button key={item.id} className="text-on-surface-variant hover:text-on-surface w-full hover:bg-surface-container-high flex items-center h-10 px-2 rounded-sm transition-colors">
            <span className="material-symbols-outlined">{item.icon}</span>
            <span className="ml-4 font-label-caps text-label-caps opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{item.label}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
