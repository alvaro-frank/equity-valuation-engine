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
import { formatFinancialPeriod } from '@/common/utils/formatters';

interface FcfYieldChartProps {
  data: ChartDataPoint[];
}

export function FcfYieldChart({ data }: FcfYieldChartProps) {
  const { t } = useTranslation();

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
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
            tickFormatter={(value) => `${value}%`}
          />
          <Tooltip 
            cursor={{ fill: 'var(--on-surface)', opacity: 0.05 }}
            contentStyle={{ 
              backgroundColor: 'var(--surface-container-high)', 
              borderColor: 'var(--outline-variant)',
              borderRadius: '8px',
              color: 'var(--on-surface)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any, name: string) => {
              const labelMap: Record<string, string> = {
                fcfYield: t('financials.charts.fcf_yield_title', 'FCF Yield')
              };
              return [`${Number(value).toFixed(2)}%`, labelMap[name] || name];
            }}
          />
          <Legend 
            verticalAlign="bottom"
            iconType="circle"
            formatter={(value) => {
              const labelMap: Record<string, string> = {
                fcfYield: t('financials.charts.fcf_yield_title', 'FCF Yield')
              };
              return labelMap[value] || value;
            }}
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
          />
          <Bar dataKey="fcfYield" fill="var(--primary)" radius={[4, 4, 0, 0]} maxBarSize={40} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
