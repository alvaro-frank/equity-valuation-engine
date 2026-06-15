import { useState, useEffect, useCallback } from 'react';

export interface SearchHistoryItem {
  ticker: string;
  name?: string;
}

export function useSearchHistory() {
  const [history, setHistory] = useState<SearchHistoryItem[]>([]);

  const loadHistory = useCallback(() => {
    const saved = localStorage.getItem('searchHistoryV2');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch {
        // ignore
      }
    } else {
      // Migrate old history format if V2 doesn't exist
      const old = localStorage.getItem('searchHistory');
      if (old) {
        try {
          const oldArr: string[] = JSON.parse(old);
          const newArr = oldArr.map(ticker => ({ ticker }));
          setHistory(newArr);
          localStorage.setItem('searchHistoryV2', JSON.stringify(newArr));
          localStorage.removeItem('searchHistory'); // Clean up old format after migrating
        } catch {
          // ignore
        }
      }
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadHistory();
    const handleStorage = () => loadHistory();
    window.addEventListener('searchHistoryUpdated', handleStorage);
    return () => window.removeEventListener('searchHistoryUpdated', handleStorage);
  }, [loadHistory]);

  const addSearch = (ticker: string, name?: string) => {
    try {
      const saved = localStorage.getItem('searchHistoryV2');
      const prev: SearchHistoryItem[] = saved ? JSON.parse(saved) : [];
      
      const filtered = prev.filter(item => item.ticker !== ticker);
      const existingName = prev.find(i => i.ticker === ticker)?.name;
      const newHistory = [{ ticker, name: name || existingName }, ...filtered].slice(0, 5);
      
      localStorage.setItem('searchHistoryV2', JSON.stringify(newHistory));
      setHistory(newHistory);
      window.dispatchEvent(new Event('searchHistoryUpdated'));
    } catch { /* ignore */ }
  };

  const updateSearchName = (ticker: string, name: string) => {
    try {
      const saved = localStorage.getItem('searchHistoryV2');
      const prev: SearchHistoryItem[] = saved ? JSON.parse(saved) : [];
      
      const itemToUpdate = prev.find(i => i.ticker === ticker);
      if (!itemToUpdate || itemToUpdate.name === name) return;
      
      const newHistory = prev.map(item => item.ticker === ticker ? { ...item, name } : item);
      localStorage.setItem('searchHistoryV2', JSON.stringify(newHistory));
      setHistory(newHistory);
      window.dispatchEvent(new Event('searchHistoryUpdated'));
    } catch { /* ignore */ }
  };

  const clearHistory = () => {
    localStorage.removeItem('searchHistoryV2');
    localStorage.removeItem('searchHistory'); // Also clear old format if it somehow stuck around
    setHistory([]);
    window.dispatchEvent(new Event('searchHistoryUpdated'));
  };

  return { history, addSearch, updateSearchName, clearHistory };
}
