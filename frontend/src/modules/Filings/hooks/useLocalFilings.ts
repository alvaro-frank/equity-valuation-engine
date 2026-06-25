import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

export function useLocalFilings(ticker: string, enabled: boolean = true) {
  return useQuery({
    queryKey: ['local_filings', ticker],
    queryFn: () => ValuationApi.getLocalFilings(ticker),
    enabled: enabled && !!ticker,
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: 1,
  });
}
