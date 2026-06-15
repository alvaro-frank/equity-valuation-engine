import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import { useTranslation } from 'react-i18next';

export const useQualitativeData = (ticker: string, isValid: boolean = true) => {
  const { i18n } = useTranslation();
  
  return useQuery({
    queryKey: ['valuation', 'qualitative', ticker, i18n.language],
    queryFn: () => ValuationApi.getQualitative(ticker),
    enabled: !!ticker && isValid, // Only run if a ticker is provided and valid
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });
};
