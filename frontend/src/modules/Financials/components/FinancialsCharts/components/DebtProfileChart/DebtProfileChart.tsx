import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { formatLargeCurrency } from '@/common/utils/formatters';
import { useTranslation } from 'react-i18next';

interface DebtProfileChartProps {
  data: ChartDataPoint[];
}

export function DebtProfileChart({ data }: DebtProfileChartProps) {
  const { t } = useTranslation();
  
  const debtEbitdaName = t('financials.charts.debt_ebitda', 'Debt/EBITDA');
  
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--outline-variant)" />
          <XAxis 
            dataKey="period" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }} 
            dy={10}
          />
          <YAxis 
            yAxisId="left"
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(value) => formatLargeCurrency(value)}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(value) => `${value}x`}
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
            formatter={(value: any, name: any) => {
              if (name === debtEbitdaName) return [`${Number(value).toFixed(2)}x`, name];
              return [formatLargeCurrency(Number(value)), name];
            }}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar 
            yAxisId="left"
            dataKey="totalDebt" 
            name={t('financials.charts.total_debt', 'Total Debt')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            yAxisId="left"
            dataKey="cashAndEquivalents" 
            name={t('financials.charts.cash_and_equivalents', 'Cash & Equivalents')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="debtToEbitda"
            name={debtEbitdaName}
            stroke="var(--secondary)"
            strokeWidth={3}
            dot={{ r: 4, strokeWidth: 2, fill: 'var(--surface)' }}
            activeDot={{ r: 6 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
