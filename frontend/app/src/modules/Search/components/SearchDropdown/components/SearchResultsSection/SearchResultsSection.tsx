import type { SearchDropdownProps } from '../../SearchDropdown';
import { SearchResultsList } from '../SearchResultsList';

export function SearchResultsSection({ searchResults, isFetching, searchTerm, selectedIndex, onSelect, onHover, show, filteredHistory, onClearHistory }: SearchDropdownProps) {
  return (
    <>
      <div className="px-4 py-2 text-xs font-bold text-on-surface-variant bg-surface-container-highest border-b border-outline-variant uppercase tracking-wider flex justify-between items-center">
        <span>SEARCH RESULTS</span>
        {isFetching ? <span className="material-symbols-outlined animate-spin text-[14px]">refresh</span> : null}
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        <SearchResultsList 
          searchResults={searchResults}
          isFetching={isFetching}
          searchTerm={searchTerm}
          selectedIndex={selectedIndex}
          onSelect={onSelect}
          onHover={onHover}
          show={show}
          filteredHistory={filteredHistory}
          onClearHistory={onClearHistory}
        />
      </div>
    </>
  );
}
