import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

export const useQuantitativeData = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'quantitative', ticker],
    queryFn: () => ValuationApi.getQuantitative(ticker),
    enabled: !!ticker, // Only run if a ticker is provided
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });
};
