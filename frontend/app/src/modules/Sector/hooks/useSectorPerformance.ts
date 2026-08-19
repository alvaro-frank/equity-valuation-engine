import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

export const useSectorPerformance = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'sector-performance', ticker],
    queryFn: () => ValuationApi.getSectorPerformance(ticker),
    enabled: !!ticker,
    staleTime: 60 * 60 * 1000, // 1 hour cache since performance data changes slowly
  });
};
