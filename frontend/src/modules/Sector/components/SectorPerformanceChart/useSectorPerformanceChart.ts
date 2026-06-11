import { useMemo } from 'react';
import type { SectorPerformanceData } from '@/common/types/valuation';

export function useSectorPerformanceChart(data?: SectorPerformanceData) {
  const formattedData = useMemo(() => {
    if (!data || !data.chart_data || data.chart_data.length === 0) return [];
    
    // Sample data to 1 point per month to make the chart rendering extremely fast
    const sampledData = [];
    let lastMonth = -1;
    for (const point of data.chart_data) {
       const date = new Date(point.date);
       if (date.getMonth() !== lastMonth) {
           sampledData.push({
               ...point,
               formattedDate: date.toLocaleDateString(undefined, { year: '2-digit', month: 'short' })
           });
           lastMonth = date.getMonth();
       }
    }
    return sampledData;
  }, [data]);

  const hasData = !!data && formattedData.length > 0;
  const etfTicker = data?.etf_ticker || '';
  const benchmarkTicker = data?.benchmark_ticker || '';

  return { formattedData, hasData, etfTicker, benchmarkTicker };
}
