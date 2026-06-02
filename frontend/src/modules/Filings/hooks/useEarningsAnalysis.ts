import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/common/utils/api';

export function useEarningsAnalysis() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ ticker, file }: { ticker: string; file: File }) => {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post(`/valuation/earnings/${ticker}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['earnings_analysis', variables.ticker], data);
    }
  });
}
