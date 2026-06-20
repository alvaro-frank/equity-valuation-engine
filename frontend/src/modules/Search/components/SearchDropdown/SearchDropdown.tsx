
export interface SearchDropdownProps {
  show: boolean;
  searchTerm: string;
  isFetching: boolean;
  searchResults: Array<{ symbol: string; name: string; exchange: string }> | undefined;
  filteredHistory: Array<{ ticker: string; name?: string }>;
  selectedIndex: number;
  onSelect: (ticker: string, name?: string) => void;
  onHover: (index: number) => void;
  onClearHistory: () => void;
  className?: string;
}

import { SearchResultsSection } from './components/SearchResultsSection';
import { RecentSearchesSection } from './components/RecentSearchesSection';

// --- Main Component ---

export function SearchDropdown(props: SearchDropdownProps) {
  const { show, searchTerm, filteredHistory, searchResults, isFetching, selectedIndex, onSelect, onHover, onClearHistory, className } = props;
  const hasSearchTerm = searchTerm.trim().length > 0;
  
  if (!show) return null;
  if (!hasSearchTerm && filteredHistory.length === 0) return null;

  return (
    <div className={`bg-surface-container-high border border-outline-variant rounded-xl shadow-2xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200 ${className || ''}`}>
      {hasSearchTerm ? (
        <SearchResultsSection 
          show={show} 
          searchTerm={searchTerm} 
          filteredHistory={filteredHistory}
          searchResults={searchResults}
          isFetching={isFetching}
          selectedIndex={selectedIndex}
          onSelect={onSelect}
          onHover={onHover}
          onClearHistory={onClearHistory}
        />
      ) : (
        <RecentSearchesSection 
          show={show} 
          searchTerm={searchTerm} 
          filteredHistory={filteredHistory}
          searchResults={searchResults}
          isFetching={isFetching}
          selectedIndex={selectedIndex}
          onSelect={onSelect}
          onHover={onHover}
          onClearHistory={onClearHistory}
        />
      )}
    </div>
  );
}
