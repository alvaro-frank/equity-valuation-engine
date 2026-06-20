import { useTranslation } from 'react-i18next';
import { SearchHistoryItem } from '../../../SearchHistoryItem';
import type { SearchDropdownProps } from '../../SearchDropdown';

export function RecentSearchesSection({ onClearHistory, filteredHistory, selectedIndex, onSelect, onHover }: SearchDropdownProps) {
  const { t } = useTranslation();
  return (
    <>
      <div className="px-4 py-2 text-xs font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant flex justify-between items-center">
        <span>{t('search.recent_searches')}</span>
        <button 
          type="button"
          onMouseDown={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onClearHistory();
          }}
          className="text-error hover:text-error/80 cursor-pointer transition-colors"
        >
          {t('search.clear')}
        </button>
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        {filteredHistory.map((item, index) => (
          <SearchHistoryItem
            key={item.ticker}
            ticker={item.ticker}
            name={item.name}
            isSelected={index === selectedIndex}
            onSelect={() => onSelect(item.ticker, item.name)}
            onHover={() => onHover(index)}
            className="px-4 py-3 text-base"
          />
        ))}
      </div>
    </>
  );
}
