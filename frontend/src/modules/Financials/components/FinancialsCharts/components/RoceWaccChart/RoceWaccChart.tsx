import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { useTranslation } from 'react-i18next';

interface RoceWaccChartProps {
  data: ChartDataPoint[];
}

export function RoceWaccChart({ data }: RoceWaccChartProps) {
  const { t } = useTranslation();
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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
            tickFormatter={(value) => `${value}%`}
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
            formatter={(value: any, name: any) => [`${Number(value)}%`, name]}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
            iconType="circle"
          />
          <Bar 
            dataKey="roic" 
            name={t('financials.charts.roce', 'ROCE')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            dataKey="wacc" 
            name={t('financials.charts.wacc', 'WACC')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
