import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

export const useQuantitativeData = (ticker: string, isValid: boolean = true) => {
  return useQuery({
    queryKey: ['valuation', 'quantitative', ticker],
    queryFn: () => ValuationApi.getQuantitative(ticker),
    enabled: !!ticker && isValid, // Only run if a ticker is provided and valid
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });
};
