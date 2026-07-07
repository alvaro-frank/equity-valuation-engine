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

interface CashFlowCapexChartProps {
  data: ChartDataPoint[];
}

export function CashFlowCapexChart({ data }: CashFlowCapexChartProps) {
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
            formatter={(value: any) => [formatLargeCurrency(Number(value))]}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar 
            dataKey="capEx" 
            name={t('financials.charts.capital_expenditures', 'Capital Expenditures')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            dataKey="operatingCashFlow" 
            name={t('financials.charts.operating_cash_flow', 'Operating Cash Flow')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
