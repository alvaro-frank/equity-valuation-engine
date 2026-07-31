import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { formatCurrency, formatFinancialPeriod } from '@/common/utils/formatters';
import { useTranslation } from 'react-i18next';

interface EpsChartProps {
  data: ChartDataPoint[];
}

export function EpsChart({ data }: EpsChartProps) {
  const { t } = useTranslation();

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--outline-variant)" opacity={0.3} />
          <XAxis 
            dataKey="period" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            dy={10}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(val) => formatCurrency(val)}
            dx={-10}
          />
          <Tooltip
            cursor={{ stroke: 'var(--on-surface)', strokeWidth: 1, strokeDasharray: '3 3', opacity: 0.2 }}
            contentStyle={{
              backgroundColor: 'var(--surface-container-high)',
              borderColor: 'var(--outline-variant)',
              borderRadius: '8px',
              color: 'var(--on-surface)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any) => [formatCurrency(value), t('financials.metrics.eps', 'EPS')]}
          />
          
          <Line 
            type="monotone" 
            dataKey="eps" 
            stroke="var(--primary)" 
            strokeWidth={3}
            dot={{ r: 4, fill: 'var(--primary)', strokeWidth: 0 }}
            activeDot={{ r: 6, fill: 'var(--primary)', strokeWidth: 0 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
