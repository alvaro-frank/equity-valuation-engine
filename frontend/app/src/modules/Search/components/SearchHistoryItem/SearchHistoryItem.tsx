import { CompanyLogo } from '@/common/components/CompanyLogo';

interface SearchHistoryItemProps {
  ticker: string;
  name?: string;
  isSelected: boolean;
  onSelect: () => void;
  onHover: () => void;
  className?: string;
}

export function SearchHistoryItem({ ticker, name, isSelected, onSelect, onHover, className = '' }: SearchHistoryItemProps) {
  return (
    <div 
      className={`px-3 py-2 text-sm text-on-surface cursor-pointer flex items-center transition-colors ${isSelected ? 'bg-surface-container-highest' : 'hover:bg-surface-container-highest'} ${className}`}
      onMouseDown={(e) => {
        e.preventDefault();
        onSelect();
      }}
      onMouseEnter={onHover}
    >
      <span className="material-symbols-outlined text-[14px] text-outline mr-2">history</span>
      <div className="flex items-center gap-2">
        <CompanyLogo ticker={ticker} className="w-5 h-5 text-[10px]" fallbackLetter={ticker[0]} />
        <span className="font-data-mono font-medium">{ticker}</span>
        {name ? <span className="text-[10px] text-on-surface-variant ml-1 truncate max-w-[120px]">- {name}</span> : null}
      </div>
    </div>
  );
}
