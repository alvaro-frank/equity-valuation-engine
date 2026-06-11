import { useState, useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useEarningsAnalysis } from './useEarningsAnalysis';
import { parseApiError } from '@/common/utils/apiErrors';

export function useFilingsView(ticker: string) {
  const { t, i18n } = useTranslation();
  const queryClient = useQueryClient();
  const { mutate, data: mutationData, isPending, error, reset } = useEarningsAnalysis();
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [currentLang, setCurrentLang] = useState<string>(i18n.language);

  // Reset mutation state when language changes so mutationData doesn't override cachedData
  if (currentLang !== i18n.language) {
    setCurrentLang(i18n.language);
    reset();
  }

  const cachedData = queryClient.getQueryData(['earnings_analysis', ticker, i18n.language]);
  const activeData = cachedData || mutationData;

  // Auto-fetch if we have a file but no data for the new language
  useEffect(() => {
    if (selectedFile && !activeData && !isPending && !error) {
      mutate({ ticker, file: selectedFile });
    }
  }, [i18n.language, selectedFile, activeData, isPending, error, mutate, ticker]);

  const handleReset = () => {
    reset();
    setSelectedFile(null);
    queryClient.removeQueries({ queryKey: ['earnings_analysis', ticker, i18n.language] });
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    mutate({ ticker, file });
  };

  const getErrorState = () => {
    if (!error) return null;
    return parseApiError(error, t, ticker);
  };

  return {
    t,
    activeData,
    isPending,
    errorState: getErrorState(),
    handleFileSelect,
    handleReset
  };
}
