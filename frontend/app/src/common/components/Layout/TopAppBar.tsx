import { useTranslation } from 'react-i18next';
import { ThemeToggle } from '@/common/components/ThemeToggle/ThemeToggle';

interface TopAppBarProps {
  activeTicker?: string;
  searchComponent?: React.ReactNode;
}

export function TopAppBar({ searchComponent }: TopAppBarProps) {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === 'pt' ? 'en' : 'pt');
  };

  return (
    <header className="h-16 border-b border-outline-variant bg-surface-container-lowest flex items-center px-4 justify-between sticky top-0 z-50">
      
      {/* Empty Left Placeholder (Balances the right Actions to keep Search centered) */}
      <div className="w-64" />

      {/* Global Search Component */}
      <div className="flex-1 max-w-xl mx-4">
        {searchComponent}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-4 w-64 justify-end">
        <button 
          onClick={toggleLanguage}
          className="flex items-center justify-center w-8 h-8 rounded hover:bg-surface-container-highest transition-colors font-bold text-xs"
          title="Toggle Language"
        >
          {i18n.language === 'pt' ? 'PT' : 'EN'}
        </button>
        <div className="flex gap-2 items-center">
          <ThemeToggle className="w-8 h-8 !p-1 !rounded" />
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">notifications</span>
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">history</span>
          <span className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-highest transition-colors cursor-pointer p-1 rounded">settings</span>
        </div>
        <div className="w-6 h-6 rounded-full overflow-hidden border border-outline-variant flex items-center justify-center bg-surface-container-high text-[10px] font-bold text-on-surface">
          AF
        </div>
      </div>
    </header>
  );
}
