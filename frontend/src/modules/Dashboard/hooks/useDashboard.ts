import { useEffect } from 'react';
import { useQuantitativeData } from '@/common/api/hooks/useQuantitativeData';
import { useQualitativeData } from '@/common/api/hooks/useQualitativeData';
import { useSearchHistory } from '@/modules/Search/hooks/useSearchHistory';
import { useTickerValidation } from '@/common/api/hooks/useTickerValidation';

export function useDashboard(ticker: string, isParentError?: boolean, onErrorChange?: (hasError: boolean) => void) {
  const { 
    isSuccess: isValid, 
    isLoading: isVerifying, 
    error: validationError,
    refetch: refetchValidation
  } = useTickerValidation(ticker);
  const { 
    data: quantData, 
    isLoading: isLoadingQuant, 
    error: errorQuant,
    refetch: refetchQuant
  } = useQuantitativeData(ticker, isValid);

  const { 
    data: qualData, 
    isLoading: isLoadingQual, 
    error: errorQual,
    refetch: refetchQual
  } = useQualitativeData(ticker, isValid);

  const { updateSearchName } = useSearchHistory();

  useEffect(() => {
    if (qualData?.ticker?.name) {
      updateSearchName(ticker, qualData.ticker.name);
    }
  }, [qualData?.ticker?.name, ticker, updateSearchName]);

  const hasError = !!validationError || !!errorQuant || !!errorQual;

  useEffect(() => {
    if (hasError !== isParentError) {
      onErrorChange?.(hasError);
    }
  }, [hasError, isParentError, onErrorChange]);

  const isLoading = isVerifying || isLoadingQuant || isLoadingQual;

  const retry = () => {
    if (validationError) refetchValidation();
    if (errorQuant) refetchQuant();
    if (errorQual) refetchQual();
  };

  return {
    quantData,
    qualData,
    isLoading,
    hasError,
    errorQuant: validationError || errorQuant,
    errorQual: validationError || errorQual,
    retry
  };
}
