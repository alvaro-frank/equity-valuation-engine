
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
import { useTranslation } from 'react-i18next';
import { useSectorPerformanceChart } from './useSectorPerformanceChart';

// --- Sub-Components (Rule 2.23) ---

function NoDataState() {
  return (
    <div className="h-full flex items-center justify-center text-on-surface-variant p-8 bg-surface-container-low border border-outline-variant rounded-xl">
      No performance data available
    </div>
  );
}

interface ChartHeaderProps {
  etfTicker: string;
  benchmarkTicker: string;
}

function ChartHeader({ etfTicker, benchmarkTicker }: ChartHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
      <div>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('sector_view.market_momentum', 'Relative Market Momentum (5Y)')}
        </h3>
        <p className="text-body-sm text-on-surface-variant">
          {t('sector_view.market_momentum_desc', 'Comparing Sector ETF performance vs Benchmark')}
        </p>
      </div>
      <div className="flex gap-2">
        <span className="text-xs px-2 py-1 bg-surface-container text-primary font-bold border border-outline-variant rounded">
          {etfTicker}
        </span>
        <span className="text-xs px-2 py-1 bg-surface-container text-secondary font-bold border border-outline-variant rounded">
          {benchmarkTicker}
        </span>
      </div>
    </div>
  );
}

// --- Main Component ---

interface SectorPerformanceChartProps {
  data?: SectorPerformanceData;
}

export function SectorPerformanceChart({ data }: SectorPerformanceChartProps) {
  const { formattedData, hasData, etfTicker, benchmarkTicker } = useSectorPerformanceChart(data);

  if (!hasData) {
    return <NoDataState />;
  }

  return (
    <div className="bg-surface-container-low border border-outline-variant rounded-xl overflow-hidden h-[400px] flex flex-col w-full">
      <ChartHeader etfTicker={etfTicker} benchmarkTicker={benchmarkTicker} />
      <div className="p-4 flex-1 min-h-0 min-w-0">
        <ResponsiveContainer width="99%" height="100%" debounce={300}>
          <LineChart data={formattedData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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
              iconType="circle" 
              wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px' }}
            />
            <Line 
              type="monotone" 
              dataKey={etfTicker} 
              name={`Sector (${etfTicker})`} 
              stroke="var(--primary)" 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
            <Line 
              type="monotone" 
              dataKey={benchmarkTicker} 
              name={`Benchmark (${benchmarkTicker})`} 
              stroke="var(--secondary)" 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, strokeWidth: 0 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
