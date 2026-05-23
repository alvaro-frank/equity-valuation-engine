import { useQuery, useMutation } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';

// Custom Hook to fetch Quantitative Data
export const useQuantitativeData = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'quantitative', ticker],
    queryFn: () => ValuationApi.getQuantitative(ticker),
    enabled: !!ticker, // Only run if a ticker is provided
    staleTime: 5 * 60 * 1000, // 5 minutes cache
  });
};

// Custom Hook to fetch Qualitative Data
export const useQualitativeData = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'qualitative', ticker],
    queryFn: () => ValuationApi.getQualitative(ticker),
    enabled: !!ticker,
    staleTime: 30 * 60 * 1000, // 30 minutes cache
  });
};

// Custom Hook to fetch Sector Data
export const useSectorData = (ticker: string) => {
  return useQuery({
    queryKey: ['valuation', 'sector', ticker],
    queryFn: () => ValuationApi.getSector(ticker),
    enabled: !!ticker,
    staleTime: 30 * 60 * 1000,
  });
};

// Custom Mutation Hook for Uploading Earnings PDF
export const useUploadEarningsReport = () => {
  return useMutation({
    mutationFn: ({ ticker, file }: { ticker: string; file: File }) => 
      ValuationApi.uploadEarningsReport(ticker, file),
  });
};
