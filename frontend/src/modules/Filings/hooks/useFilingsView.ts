import { useState, useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useEarningsAnalysis } from './useEarningsAnalysis';
import { useLocalFilingAnalysis } from './useLocalFilingAnalysis';
import { useLocalFilings } from './useLocalFilings';
import { parseApiError } from '@/common/utils/apiErrors';
import { useQuantitativeData } from '@/common/api/hooks/useQuantitativeData';
import { useTickerValidation } from '@/common/api/hooks/useTickerValidation';
import type { LocalFilingDTO } from '@/common/types/valuation';

export function useFilingsView(ticker: string) {
  const { t, i18n } = useTranslation();
  const queryClient = useQueryClient();
  
  const { isSuccess: isValid, isLoading: isVerifying, error: validationError, refetch: refetchValidation } = useTickerValidation(ticker);
  
  const { mutate: mutateUpload, data: uploadData, isPending: isUploadPending, error: uploadError, reset: resetUpload } = useEarningsAnalysis();
  const { mutate: mutateLocal, data: localData, isPending: isLocalPending, error: localError, reset: resetLocal } = useLocalFilingAnalysis();
  
  const { data: quantData, isLoading: isQuantLoading } = useQuantitativeData(ticker, isValid);
  const { data: localFilingsResult, isLoading: isFilingsLoading } = useLocalFilings(ticker, !!quantData);

  const isInitialLoading = isVerifying || (isValid && isQuantLoading) || (isValid && !!quantData && isFilingsLoading);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analyzingFilingId, setAnalyzingFilingId] = useState<string | null>(null);
  const [analyzingPeriod, setAnalyzingPeriod] = useState<string | null>(null);
  const [currentLang, setCurrentLang] = useState<string>(i18n.language);

  // Reset mutation state when language changes so mutationData doesn't override cachedData
  if (currentLang !== i18n.language) {
    setCurrentLang(i18n.language);
    resetUpload();
    resetLocal();
  }

  const cachedData = queryClient.getQueryData(['earnings_analysis', ticker, i18n.language]);
  const activeData = cachedData || uploadData || localData;



  const handleReset = () => {
    resetUpload();
    resetLocal();
    setSelectedFile(null);
    setAnalyzingFilingId(null);
    setAnalyzingPeriod(null);
    queryClient.removeQueries({ queryKey: ['earnings_analysis', ticker, i18n.language] });
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setAnalyzingFilingId(null);
    setAnalyzingPeriod(null);
    mutateUpload({ ticker, file });
  };

  const handleLocalFilingSelect = (filing: LocalFilingDTO) => {
    setSelectedFile(null);
    setAnalyzingFilingId(filing.id);
    setAnalyzingPeriod(filing.period);
    mutateLocal({ ticker, filePath: filing.id, focusPeriod: filing.focus_period });
  };

  const getErrorState = () => {
    const err = uploadError || localError;
    if (!err) return null;
    return parseApiError(err, t, ticker);
  };

  const getValidationErrorState = () => {
    if (!validationError) return null;
    return parseApiError(validationError, t, ticker);
  };

  return {
    t,
    isValid,
    isInitialLoading,
    validationErrorState: getValidationErrorState(),
    activeData,
    quantData,
    localFilings: localFilingsResult?.filings || [],
    isPending: isUploadPending || isLocalPending,
    analyzingFilingId,
    analyzingPeriod,
    errorState: getErrorState(),
    handleFileSelect,
    handleLocalFilingSelect,
    handleReset
  };
}
