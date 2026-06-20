
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import type { SectorPerformanceData } from '@/common/types/valuation';
import { useSectorPerformanceChart } from './useSectorPerformanceChart';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { NoDataState } from './components/NoDataState';
import { ChartHeader } from './components/ChartHeader';

// --- Main Component ---

interface SectorPerformanceChartProps {
  data?: SectorPerformanceData;
  companyName?: string;
}

export function SectorPerformanceChart({ data, companyName }: SectorPerformanceChartProps) {
  const { formattedData, hasData, companyTicker, sector, industry, sectorEtf, industryEtf, benchmarkTicker, hiddenLines, handleLegendClick } = useSectorPerformanceChart(data);

  if (!hasData) {
    return <NoDataState />;
  }

  return (
    <div className="bg-surface-container-low border border-outline-variant rounded-xl overflow-hidden h-[400px] flex flex-col w-full">
      <ChartHeader companyTicker={companyTicker} companyName={companyName} sector={sector} industry={industry} benchmarkTicker={benchmarkTicker} />
      <div className="p-4 flex-1 min-h-0 min-w-0">
        <ResponsiveContainer width="99%" height="100%" debounce={300}>
          <LineChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--outline-variant)" vertical={false} />
            <XAxis 
              dataKey="formattedDate" 
              stroke="var(--outline)" 
              fontSize={11} 
              tickLine={false} 
              axisLine={false} 
              dy={10}
              minTickGap={40}
            />
            <YAxis 
              stroke="var(--outline)" 
              fontSize={11} 
              tickLine={false} 
              axisLine={false} 
              tickFormatter={(val) => `${val}%`}
            />
            <Tooltip 
              cursor={{ stroke: 'var(--outline-variant)', strokeWidth: 1, strokeDasharray: '3 3' }}
              contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--on-surface)' }}
              formatter={(value: unknown, name: unknown) => [`${Number(value).toFixed(2)}%`, name as string]}
              labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
            />
            <Legend 
              onClick={handleLegendClick}
              iconType="circle" 
              wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px', cursor: 'pointer' }}
            />
            {companyTicker && (
              <Line 
                type="monotone" 
                dataKey={companyTicker} 
                name={`${companyName || companyTicker} (${companyTicker})`}
                stroke="var(--on-surface)" 
                strokeWidth={3}
                dot={false}
                hide={hiddenLines[companyTicker]}
                activeDot={{ r: 5, strokeWidth: 0 }}
              />
            )}
            <Line 
              type="monotone" 
              dataKey={sectorEtf} 
              name={`${translateSector(sector)} (${sectorEtf})`}
              stroke="var(--primary)" 
              strokeWidth={1.5}
              dot={false}
              hide={hiddenLines[sectorEtf]}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
            {industryEtf && (
              <Line 
                type="monotone" 
                dataKey={industryEtf} 
                name={`${translateIndustry(industry)} (${industryEtf})`}
                stroke="var(--tertiary)" 
                strokeWidth={1.5}
                dot={false}
                hide={hiddenLines[industryEtf]}
                activeDot={{ r: 4, strokeWidth: 0 }}
              />
            )}
            <Line 
              type="monotone" 
              dataKey={benchmarkTicker} 
              name={`S&P 500 (${benchmarkTicker})`}
              stroke="var(--chart-benchmark)" 
              strokeWidth={1.5}
              dot={false}
              hide={hiddenLines[benchmarkTicker]}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
