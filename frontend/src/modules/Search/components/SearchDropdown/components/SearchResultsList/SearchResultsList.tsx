import { SearchResultItem } from '../../../SearchResultItem';
import { LoadingState } from '../LoadingState';
import { EmptyState } from '../EmptyState';
import type { SearchDropdownProps } from '../../SearchDropdown';

export function SearchResultsList({ searchResults, isFetching, searchTerm, selectedIndex, onSelect, onHover }: SearchDropdownProps) {
  
  if (isFetching && (!searchResults || searchResults.length === 0)) {
    return <LoadingState />;
  }

  if (!searchResults || searchResults.length === 0) {
    return <EmptyState searchTerm={searchTerm} />;
  }

  return (
    <>
      {searchResults.map((item, index) => (
        <SearchResultItem
          key={item.symbol}
          symbol={item.symbol}
          name={item.name}
          exchange={item.exchange}
          isSelected={index === selectedIndex}
          onSelect={() => onSelect(item.symbol, item.name)}
          onHover={() => onHover(index)}
          className="px-4 py-3"
        />
      ))}
    </>
  );
}
