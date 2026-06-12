import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import { useTranslation } from 'react-i18next';

export const useQualitativeData = (ticker: string) => {
  const { i18n } = useTranslation();
  return useQuery({
    queryKey: ['valuation', 'qualitative', ticker, i18n.language],
    queryFn: () => ValuationApi.getQualitative(ticker),
    enabled: !!ticker,
    staleTime: 30 * 60 * 1000, // 30 minutes cache
  });
};
