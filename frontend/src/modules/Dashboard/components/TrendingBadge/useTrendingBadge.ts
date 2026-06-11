import { useState, useRef, useCallback, useMemo } from 'react';
import { useTrendingTickers } from '@/common/hooks/useTrendingTickers';
import { useClickOutside } from '@/common/hooks/useClickOutside';

interface UseTrendingBadgeProps {
  type: 'sector' | 'industry';
  queryKey?: string;
  currentTicker?: string;
  onSelectTicker: (ticker: string) => void;
}

export function useTrendingBadge({ type, queryKey, currentTicker, onSelectTicker }: UseTrendingBadgeProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);

  // Data fetching
  const { data, isLoading, error } = useTrendingTickers(isOpen ? type : null, queryKey || null);
  const displayData = useMemo(() => {
    return data ? data.filter((item) => item.symbol !== currentTicker) : [];
  }, [data, currentTicker]);

  // Click outside handling
  useClickOutside(
    containerRef,
    () => setIsOpen(false),
    isOpen
  );

  const handleToggle = useCallback(() => {
    if (!queryKey) return;
    setIsOpen((prev) => !prev);
  }, [queryKey]);

  const handleSelect = useCallback(
    (ticker: string) => {
      setIsOpen(false);
      setSelectedIndex(-1);
      onSelectTicker(ticker);
    },
    [onSelectTicker]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (!isOpen) return;
      const maxIndex = displayData.length - 1;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev < maxIndex ? prev + 1 : prev));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : 0));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex <= maxIndex) {
          handleSelect(displayData[selectedIndex].symbol);
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        setIsOpen(false);
        setSelectedIndex(-1);
      }
    },
    [isOpen, displayData, selectedIndex, handleSelect]
  );

  return {
    isOpen,
    selectedIndex,
    setSelectedIndex,
    containerRef,
    isLoading,
    error,
    displayData,
    handleToggle,
    handleSelect,
    handleKeyDown,
  };
}
