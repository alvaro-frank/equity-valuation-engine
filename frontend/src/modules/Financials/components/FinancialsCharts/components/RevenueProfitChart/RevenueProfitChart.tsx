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
import { formatLargeCurrency } from '@/common/utils/formatters';
import { useTranslation } from 'react-i18next';

interface RevenueProfitChartProps {
  data: ChartDataPoint[];
}

export function RevenueProfitChart({ data }: RevenueProfitChartProps) {
  const { t } = useTranslation();
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
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
            tickFormatter={(value) => formatLargeCurrency(value)}
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
            formatter={(value: any, name: any) => [formatLargeCurrency(Number(value)), name]}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar 
            dataKey="revenue" 
            name={t('financials.charts.revenue', 'Revenue')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            dataKey="ebitda" 
            name={t('financials.charts.ebitda', 'EBITDA')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            dataKey="netIncome" 
            name={t('financials.charts.net_income', 'Net Income')} 
            fill="var(--secondary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
