import { useState, useEffect } from 'react';
import { api } from '@/common/utils/api';

export interface TrendingTicker {
  symbol: string;
  name: string;
  rating?: string;
  weight?: number;
}

export function useTrendingTickers(type: 'sector' | 'industry' | null, key: string | null) {
  const [data, setData] = useState<TrendingTicker[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!type || !key) {
      return;
    }

    let isMounted = true;

    const fetchTrending = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await api.get(`/discovery/${type}/${key}/trending`);
        if (isMounted) {
          setData(response.data.results || []);
        }
      } catch (err: unknown) {
        if (isMounted) {
          setError(err instanceof Error ? err : new Error(String(err)));
          setData([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchTrending();

    return () => {
      isMounted = false;
    };
  }, [type, key]);

  return { data, isLoading, error };
}
