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
import { formatFinancialPeriod } from '@/common/utils/formatters';

interface PfcfRatioChartProps {
  data: ChartDataPoint[];
}

export function PfcfRatioChart({ data }: PfcfRatioChartProps) {
  const { t } = useTranslation();

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
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
                pfcfRatio: t('financials.charts.pfcf_ratio', 'P/FCF')
              };
              return [`${Number(value).toFixed(2)}x`, labelMap[name] || name];
            }}
          />
          <Legend 
            verticalAlign="bottom"
            iconType="circle"
            formatter={(value) => {
              const labelMap: Record<string, string> = {
                pfcfRatio: t('financials.charts.pfcf_ratio', 'P/FCF')
              };
              return labelMap[value] || value;
            }}
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
          />
          <Line 
            type="monotone" 
            dataKey="pfcfRatio" 
            stroke="var(--primary)" 
            strokeWidth={2}
            dot={{ r: 4, fill: 'var(--surface)', strokeWidth: 2 }}
            activeDot={{ r: 6 }}
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
