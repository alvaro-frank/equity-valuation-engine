import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import { useTranslation } from 'react-i18next';

export const useSectorData = (ticker: string) => {
  const { i18n } = useTranslation();
  return useQuery({
    queryKey: ['valuation', 'sector', ticker, i18n.language],
    queryFn: () => ValuationApi.getSector(ticker),
    enabled: !!ticker,
    staleTime: 30 * 60 * 1000,
  });
};
