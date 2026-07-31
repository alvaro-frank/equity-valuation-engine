import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { formatLargeCurrency } from '@/common/utils/formatters';

interface ShareholderReturnsChartProps {
  data: ChartDataPoint[];
}

export function ShareholderReturnsChart({ data }: ShareholderReturnsChartProps) {
  if (!data || data.length === 0) return null;

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 10, left: 0, bottom: 0 }}
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
            tickFormatter={(val) => formatLargeCurrency(val)}
            dx={-10}
          />
          <Tooltip
            cursor={{ fill: 'var(--on-surface)', opacity: 0.05 }}
            contentStyle={{
              backgroundColor: 'var(--surface-container-high)',
              borderColor: 'var(--outline-variant)',
              borderRadius: '8px',
              color: 'var(--on-surface)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any, name: string) => {
              const labelMap: Record<string, string> = {
                dividendsPaid: 'Dividends Paid',
                stockRepurchases: 'Stock Repurchases'
              };
              return [formatLargeCurrency(value), labelMap[name] || name];
            }}
            labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
          />
          <Legend 
            verticalAlign="bottom"
            iconType="circle"
            formatter={(value) => {
              const labelMap: Record<string, string> = {
                dividendsPaid: 'Dividends Paid',
                stockRepurchases: 'Stock Repurchases'
              };
              return labelMap[value] || value;
            }}
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
          />
          <Bar dataKey="dividendsPaid" fill="var(--primary)" radius={[4, 4, 0, 0]} maxBarSize={40} />
          <Bar dataKey="stockRepurchases" fill="var(--tertiary)" radius={[4, 4, 0, 0]} maxBarSize={40} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
