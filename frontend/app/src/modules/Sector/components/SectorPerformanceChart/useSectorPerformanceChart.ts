import { useMemo, useState, useCallback } from 'react';
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
  const companyTicker = data?.company_ticker || '';
  const sector = data?.sector || '';
  const industry = data?.industry || '';
  const sectorEtf = data?.sector_etf || '';
  const industryEtf = data?.industry_etf;
  const benchmarkTicker = data?.benchmark_ticker || '';

  const [hiddenLines, setHiddenLines] = useState<Record<string, boolean>>({});

  const handleLegendClick = useCallback((e: any) => {
    const dataKey = e.dataKey;
    if (dataKey) {
      setHiddenLines(prev => ({
        ...prev,
        [dataKey]: !prev[dataKey]
      }));
    }
  }, []);

  return { formattedData, hasData, companyTicker, sector, industry, sectorEtf, industryEtf, benchmarkTicker, hiddenLines, handleLegendClick };
}
