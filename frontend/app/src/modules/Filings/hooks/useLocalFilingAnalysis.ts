import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import { useTranslation } from 'react-i18next';

export function useLocalFilingAnalysis() {
  const queryClient = useQueryClient();
  const { i18n } = useTranslation();

  return useMutation({
    mutationFn: async ({ ticker, filePath, focusPeriod }: { ticker: string; filePath: string; focusPeriod?: string }) => {
      return await ValuationApi.analyseLocalFiling(ticker, filePath, focusPeriod);
    },
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['earnings_analysis', variables.ticker, i18n.language], data);
    }
  });
}
