import { useQuery } from '@tanstack/react-query';
import { api } from '../utils/api';

export interface TickerSearchDTO {
  symbol: string;
  name: string;
  exchange: string;
}

export interface TickerSearchResult {
  results: TickerSearchDTO[];
}

export function useSearchTickers(query: string) {
  return useQuery({
    queryKey: ['search', query],
    queryFn: async (): Promise<TickerSearchDTO[]> => {
      if (!query) return [];
      const response = await api.get<TickerSearchResult>(`/valuation/search?q=${encodeURIComponent(query)}`);
      return response.data.results;
    },
    enabled: query.length > 0,
    staleTime: 60 * 1000 * 5, // 5 minutes
  });
}
