import { useEffect } from 'react';
import { useQuantitativeData } from '@/common/hooks/useQuantitativeData';
import { useQualitativeData } from '@/common/hooks/useQualitativeData';
import { useSearchHistory } from '@/common/hooks/useSearchHistory';

export function useDashboard(ticker: string, isParentError?: boolean, onErrorChange?: (hasError: boolean) => void) {
  const { 
    data: quantData, 
    isLoading: isLoadingQuant, 
    error: errorQuant,
    refetch: refetchQuant
  } = useQuantitativeData(ticker);

  const { 
    data: qualData, 
    isLoading: isLoadingQual, 
    error: errorQual,
    refetch: refetchQual
  } = useQualitativeData(ticker);

  const { updateSearchName } = useSearchHistory();

  useEffect(() => {
    if (qualData?.ticker?.name) {
      updateSearchName(ticker, qualData.ticker.name);
    }
  }, [qualData?.ticker?.name, ticker, updateSearchName]);

  const hasError = !!errorQuant || !!errorQual;

  useEffect(() => {
    if (hasError !== isParentError) {
      onErrorChange?.(hasError);
    }
  }, [hasError, isParentError, onErrorChange]);

  const isLoading = isLoadingQuant || isLoadingQual;

  const retry = () => {
    if (errorQuant) refetchQuant();
    if (errorQual) refetchQual();
  };

  return {
    quantData,
    qualData,
    isLoading,
    hasError,
    errorQuant,
    errorQual,
    retry
  };
}
