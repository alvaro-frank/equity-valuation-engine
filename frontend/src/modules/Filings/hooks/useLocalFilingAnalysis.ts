import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import { useTranslation } from 'react-i18next';

export function useLocalFilingAnalysis() {
  const queryClient = useQueryClient();
  const { i18n } = useTranslation();

  return useMutation({
    mutationFn: async ({ ticker, filePath }: { ticker: string; filePath: string }) => {
      return await ValuationApi.analyseLocalFiling(ticker, filePath);
    },
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['earnings_analysis', variables.ticker, i18n.language], data);
    }
  });
}
