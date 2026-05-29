import { useState, useEffect } from 'react';
import { useSearchHistory } from './useSearchHistory';
import { useDebounce } from './useDebounce';
import { useSearchTickers } from './useSearchTickers';

export function useSearchBox(onSearchCallback?: (ticker: string) => void) {
  const [searchTerm, setSearchTerm] = useState('');
  const { history: searchHistory, addSearch, clearHistory } = useSearchHistory();
  const [showHistory, setShowHistory] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const debouncedSearchTerm = useDebounce(searchTerm.trim(), 300);
  const { data: searchResults, isFetching: isSearchingAPI } = useSearchTickers(debouncedSearchTerm);

  const isSearching = searchTerm.trim().length > 0;

  const filteredHistory = searchHistory.filter(item => {
    const term = searchTerm.toLowerCase();
    return item.ticker.toLowerCase().includes(term) || (item.name && item.name.toLowerCase().includes(term));
  });

  const noResults = isSearching && searchResults?.length === 0 && !isSearchingAPI;
  const isSearchDisabled = !searchTerm.trim() || noResults;

  useEffect(() => {
    if (!showHistory) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSelectedIndex(-1);
    }
  }, [showHistory]);

  const handleSearch = (termToSearch: string = searchTerm, companyName?: string) => {
    if (termToSearch.trim()) {
      const upperTerm = termToSearch.toUpperCase();
      onSearchCallback?.(upperTerm);
      addSearch(upperTerm, companyName);
      setSearchTerm('');
      setShowHistory(false);
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const maxIndex = isSearching && searchResults ? searchResults.length - 1 : filteredHistory.length - 1;
    
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => (prev < maxIndex ? prev + 1 : prev));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => (prev > -1 ? prev - 1 : -1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && selectedIndex <= maxIndex) {
        if (isSearching && searchResults) {
          handleSearch(searchResults[selectedIndex].symbol, searchResults[selectedIndex].name);
        } else {
          handleSearch(filteredHistory[selectedIndex].ticker, filteredHistory[selectedIndex].name);
        }
      } else if (!isSearchDisabled) {
        handleSearch();
      }
    } else if (e.key === 'Escape') {
      setShowHistory(false);
      setSelectedIndex(-1);
    }
  };

  const handleFocus = () => setShowHistory(true);
  const handleBlur = () => setTimeout(() => setShowHistory(false), 200);

  return {
    searchTerm,
    setSearchTerm,
    showHistory,
    setShowHistory,
    selectedIndex,
    setSelectedIndex,
    searchResults,
    filteredHistory,
    isSearchingAPI,
    isSearching,
    isSearchDisabled,
    handleSearch,
    handleKeyDown,
    handleFocus,
    handleBlur,
    clearHistory
  };
}
