import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useTranslation } from 'react-i18next';
import { formatPercentage } from '@/common/utils/formatters';

export interface MarginDataPoint {
  label: string;
  grossMargin: number;
  opMargin: number | null;
  netMargin: number | null;
  isTTM?: boolean;
}

interface MarginLineChartProps {
  data: MarginDataPoint[];
}

export function MarginLineChart({ data }: MarginLineChartProps) {
  const { t } = useTranslation();
  
  if (!data.length) {
    return (
      <div className="h-full flex items-center justify-center text-on-surface-variant">
        No data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="99%" height="100%" debounce={300}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--outline-variant)" vertical={false} />
        <XAxis 
          dataKey="label" 
          stroke="var(--outline)" 
          fontSize={11} 
          tickLine={false} 
          axisLine={false} 
          dy={5}
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
          contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)' }}
          itemStyle={{ color: 'var(--on-surface)' }}
          formatter={(value: unknown, name: unknown) => [formatPercentage(Number(value)), String(name)]}
          labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
        />
        <Legend 
          iconType="plainline" 
          wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px' }}
        />
        <Line 
          type="monotone" 
          dataKey="grossMargin" 
          name={t('dashboard.gross_margin')} 
          stroke="var(--primary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--primary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
        <Line 
          type="monotone" 
          dataKey="opMargin" 
          name={t('dashboard.operating_margin')} 
          stroke="var(--secondary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--secondary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
        <Line 
          type="monotone" 
          dataKey="netMargin" 
          name={t('dashboard.net_margin', 'NET MARGIN')} 
          stroke="var(--tertiary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--tertiary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
