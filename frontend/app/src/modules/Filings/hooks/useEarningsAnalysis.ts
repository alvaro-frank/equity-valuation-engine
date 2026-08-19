import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/common/utils/api';
import { useTranslation } from 'react-i18next';

export function useEarningsAnalysis() {
  const queryClient = useQueryClient();
  const { i18n } = useTranslation();

  return useMutation({
    mutationFn: async ({ ticker, file }: { ticker: string; file: File }) => {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post(`/valuation/earnings/${ticker}`, formData, {
        params: { lang: i18n.language },
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['earnings_analysis', variables.ticker, i18n.language], data);
    }
  });
}
