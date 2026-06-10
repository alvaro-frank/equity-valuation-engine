import { useState, useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useEarningsAnalysis } from './useEarningsAnalysis';
import type { FilingsErrorDetails } from '../components/FilingsErrorState';

const getErrorDetails = (key: number | string, t: any): FilingsErrorDetails['details'] => {
  const map: Record<number | string, { title: string, message: string, icon: string }> = {
    429: {
      title: t('api_errors.429_title'),
      message: t('api_errors.429_desc'),
      icon: "hourglass_empty"
    },
    503: {
      title: t('api_errors.503_title'),
      message: t('api_errors.503_desc'),
      icon: "engineering"
    },
    DEFAULT: {
      title: t('api_errors.default_title'),
      message: t('api_errors.default_desc'),
      icon: "error_outline"
    }
  };
  return map[key] || map['DEFAULT'];
};

interface ApiError extends Error {
  response?: {
    status?: number;
    data?: { detail?: string };
  };
}

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

  const getErrorState = (): FilingsErrorDetails | null => {
    if (!error) return null;
    
    const statusCode = (error as ApiError)?.response?.status;
    const apiErrorMsg = (error as ApiError)?.response?.data?.detail || error.message || '';
    
    let errorKey: number | string = 'DEFAULT';
    
    if (statusCode === 429 || apiErrorMsg.includes('429') || apiErrorMsg.includes('RESOURCE_EXHAUSTED') || apiErrorMsg.toLowerCase().includes('quota') || apiErrorMsg === 'rate_limit_exceeded') errorKey = 429;
    else if (statusCode === 503 || apiErrorMsg.includes('503') || apiErrorMsg.includes('UNAVAILABLE') || apiErrorMsg.includes('high demand')) errorKey = 503;

    return {
      key: errorKey,
      details: getErrorDetails(errorKey, t),
      rawMessage: apiErrorMsg
    };
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
