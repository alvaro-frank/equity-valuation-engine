import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '../api/valuationApi';
import type { LiveQuoteResult } from '../types/valuation';
import { useState, useEffect } from 'react';

export function useLiveQuote(ticker: string, initialData?: { current_price?: number, regular_market_change?: number, regular_market_change_percent?: number }) {
  const [isLiveSupported, setIsLiveSupported] = useState<boolean>(true); // Start assuming it's supported so we try

  const { data: quote, isError } = useQuery<LiveQuoteResult, Error>({
    queryKey: ['liveQuote', ticker],
    queryFn: () => ValuationApi.getLiveQuote(ticker),
    refetchInterval: isLiveSupported ? 5000 : false, // Poll every 5s if supported
    enabled: !!ticker && isLiveSupported,
    staleTime: 4000, // Consider data stale after 4s
  });

  // If the server tells us it's not supported, turn off polling
  useEffect(() => {
    if (quote && !quote.is_live_supported) {
      setIsLiveSupported(false);
    }
  }, [quote]);

  // Fallback to initial data if polling hasn't returned anything yet, or if it failed
  const amount = quote?.amount ?? initialData?.current_price;
  const change = quote?.change ?? initialData?.regular_market_change;
  const changePercent = quote?.change_percent ?? initialData?.regular_market_change_percent;

  return {
    amount,
    change,
    changePercent,
    isLiveSupported: quote?.is_live_supported ?? isLiveSupported,
    isError
  };
}
