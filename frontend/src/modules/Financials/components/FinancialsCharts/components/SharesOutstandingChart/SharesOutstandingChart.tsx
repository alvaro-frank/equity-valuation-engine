import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { formatLargeNumber } from '@/common/utils/formatters';

interface SharesOutstandingChartProps {
  data: ChartDataPoint[];
}

export function SharesOutstandingChart({ data }: SharesOutstandingChartProps) {
  if (!data || data.length === 0) return null;

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.1)" />
          <XAxis 
            dataKey="period" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'rgba(255,255,255,0.7)', fontSize: 12 }}
            dy={10}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'rgba(255,255,255,0.7)', fontSize: 12 }}
            tickFormatter={(val) => formatLargeNumber(val)}
            domain={['auto', 'auto']}
          />
          <Tooltip
            contentStyle={{ 
              backgroundColor: '#1E1E24', 
              borderColor: 'rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: '#fff'
            }}
            itemStyle={{ color: '#fff' }}
            formatter={(value: any) => [formatLargeNumber(value), 'Shares']}
            labelStyle={{ color: 'rgba(255,255,255,0.7)', marginBottom: '4px' }}
          />
          <Area 
            type="monotone" 
            dataKey="sharesOutstanding" 
            name="Shares"
            stroke="var(--primary)" 
            fill="var(--primary)" 
            fillOpacity={0.3}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
