import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { useTranslation } from 'react-i18next';
import { formatFinancialPeriod } from '@/common/utils/formatters';

interface ValuationMultiplesChartProps {
  data: ChartDataPoint[];
}

export function ValuationMultiplesChart({ data }: ValuationMultiplesChartProps) {
  const { t } = useTranslation();

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--surface-border)" vertical={false} />
          <XAxis 
            dataKey="period" 
            stroke="var(--surface-border)"
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }} 
            dy={10}
            tickFormatter={(val) => formatFinancialPeriod(val, false)}
          />
          <YAxis 
            stroke="var(--surface-border)"
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(value) => `${value}x`}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'var(--surface-variant)', 
              borderColor: 'var(--surface-border)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any, name: string) => {
              const labelMap: Record<string, string> = {
                evToEbitda: t('financials.charts.ev_to_ebitda', 'EV/EBITDA'),
                peRatio: 'P/E'
              };
              return [`${Number(value).toFixed(2)}x`, labelMap[name] || name];
            }}
          />
          <Legend 
            verticalAlign="bottom"
            iconType="circle"
            formatter={(value) => {
              const labelMap: Record<string, string> = {
                evToEbitda: t('financials.charts.ev_to_ebitda', 'EV/EBITDA'),
                peRatio: 'P/E'
              };
              return labelMap[value] || value;
            }}
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
          />
          <Line 
            type="monotone" 
            dataKey="evToEbitda" 
            stroke="var(--primary)" 
            strokeWidth={2}
            dot={{ r: 4, fill: 'var(--surface)', strokeWidth: 2 }}
            activeDot={{ r: 6 }}
            connectNulls
          />
          <Line 
            type="monotone" 
            dataKey="peRatio" 
            stroke="var(--tertiary)" 
            strokeWidth={2}
            dot={{ r: 4, fill: 'var(--surface)', strokeWidth: 2 }}
            activeDot={{ r: 6 }}
            connectNulls
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
