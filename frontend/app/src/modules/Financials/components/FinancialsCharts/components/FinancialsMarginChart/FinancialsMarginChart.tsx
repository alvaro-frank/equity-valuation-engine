import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { useTranslation } from 'react-i18next';

interface FinancialsMarginChartProps {
  data: ChartDataPoint[];
}

export function FinancialsMarginChart({ data }: FinancialsMarginChartProps) {
  const { t } = useTranslation();
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--outline-variant)" />
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
            tickFormatter={(value) => `${value.toFixed(0)}%`}
          />
          <Tooltip 
            cursor={{ fill: 'var(--surface-container-highest)' }}
            contentStyle={{ 
              backgroundColor: 'var(--surface-container-high)', 
              borderColor: 'var(--outline-variant)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any, name: any) => [`${Number(value).toFixed(2)}%`, name]}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
            iconType="circle"
          />
          <Line
            type="monotone"
            dataKey="grossMargin"
            name={t('financials.charts.gross_margin', 'Gross Margin')}
            stroke="var(--primary)"
            strokeWidth={3}
            dot={{ r: 4, strokeWidth: 2, fill: 'var(--surface)' }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="operatingMargin"
            name={t('financials.charts.operating_margin', 'Operating Margin')}
            stroke="var(--tertiary)"
            strokeWidth={3}
            dot={{ r: 4, strokeWidth: 2, fill: 'var(--surface)' }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="netMargin"
            name={t('financials.charts.net_margin', 'Net Margin')}
            stroke="var(--secondary)"
            strokeWidth={3}
            dot={{ r: 4, strokeWidth: 2, fill: 'var(--surface)' }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
