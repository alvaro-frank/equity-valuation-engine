import { CompanyLogo } from '@/common/components/CompanyLogo';

interface SearchResultItemProps {
  symbol: string;
  name: string;
  exchange?: string;
  isSelected: boolean;
  onSelect: () => void;
  onHover: () => void;
  className?: string;
}

export function SearchResultItem({ symbol, name, exchange, isSelected, onSelect, onHover, className = '' }: SearchResultItemProps) {
  return (
    <div 
      className={`px-3 py-2 cursor-pointer flex items-center transition-colors ${isSelected ? 'bg-surface-container-highest' : 'hover:bg-surface-container-highest'} ${className}`}
      onMouseDown={(e) => {
        e.preventDefault();
        onSelect();
      }}
      onMouseEnter={onHover}
    >
      <span className="material-symbols-outlined text-[14px] text-outline mr-2">search</span>
      <div className="flex items-center gap-2 w-full overflow-hidden">
        <CompanyLogo ticker={symbol} className="w-5 h-5 text-[10px] shrink-0" fallbackLetter={symbol[0]} />
        <div className="flex flex-col overflow-hidden min-w-0">
          <span className="font-data-mono text-sm font-semibold text-on-surface">{symbol}</span>
          <span className="text-[10px] text-on-surface-variant truncate">{name}</span>
        </div>
        {exchange && (
          <span className="ml-auto text-[9px] text-outline px-1 rounded bg-surface-container-low uppercase whitespace-nowrap shrink-0">{exchange}</span>
        )}
      </div>
    </div>
  );
}
