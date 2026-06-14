import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

export const useTickerValidation = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'validate', ticker],
    queryFn: () => ValuationApi.validateTicker(ticker),
    enabled: !!ticker, // Only run if a ticker is provided
    staleTime: 5 * 60 * 1000, // 5 minutes cache
    retry: 0, // Do not retry validation if it fails
  });
};
