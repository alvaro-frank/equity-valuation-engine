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
import { formatLargeNumber } from '@/common/utils/formatters';
import { useTranslation } from 'react-i18next';

interface EarningsQualityChartProps {
  data: ChartDataPoint[];
}

export function EarningsQualityChart({ data }: EarningsQualityChartProps) {
  const { t } = useTranslation();

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
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
            tickFormatter={(val) => formatLargeNumber(val)}
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
            formatter={(value: any, name: any) => [formatLargeNumber(value), name]}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          
          <Bar 
            dataKey="netIncome" 
            name={t('financials.charts.net_income', 'Net Income')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
          />
          <Bar 
            dataKey="freeCashFlow" 
            name={t('financials.charts.free_cash_flow', 'Free Cash Flow')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
