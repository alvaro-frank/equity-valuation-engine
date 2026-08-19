import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';

export function useQuantitativeFallback(
  periodEndDate: string,
  quantData?: QuantitativeValuationResult
) {
  const getFallbackValue = (metricKey: string): number | null => {
    if (!quantData?.quarterly_metrics?.[metricKey]) return null;
    
    const series = quantData.quarterly_metrics[metricKey] as BaseMetric[];
    
    // yFinance and SEC dates might differ by a few days (e.g. March 28 vs March 31).
    // We match based on a 30-day window tolerance.
    const targetDate = new Date(periodEndDate).getTime();

    const matchedMetric = series.find(s => {
      const sDate = new Date(s.date).getTime();
      return Math.abs(sDate - targetDate) <= 30 * 24 * 60 * 60 * 1000;
    });

    return matchedMetric?.value ?? null;
  };

  return { getFallbackValue };
}
