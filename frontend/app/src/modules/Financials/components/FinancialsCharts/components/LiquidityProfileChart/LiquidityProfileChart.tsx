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
import { useTranslation } from 'react-i18next';
import type { ChartDataPoint } from '../../hooks/useFinancialsChartsData';
import { formatLargeCurrency } from '@/common/utils/formatters';

interface LiquidityProfileChartProps {
  data: ChartDataPoint[];
}

export function LiquidityProfileChart({ data }: LiquidityProfileChartProps) {
  const { t } = useTranslation();

  if (!data || data.length === 0) return null;

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart
          data={data}
          margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
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
            yAxisId="left"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(val) => formatLargeCurrency(val)}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            axisLine={false}
            tickLine={false}
            tick={{ fill: 'var(--on-surface-variant)', fontSize: 12 }}
            tickFormatter={(val) => `${Number(val).toFixed(1)}x`}
            domain={[0, 'auto']}
          />
          <Tooltip
            contentStyle={{ 
              backgroundColor: 'var(--surface-container-high)', 
              borderColor: 'var(--outline-variant)',
              borderRadius: '8px',
              color: 'var(--on-surface)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: any, name: any) => {
              if (name === t('financials.charts.current_ratio', 'Current Ratio')) {
                return [`${Number(value).toFixed(2)}x`, name];
              }
              return [formatLargeCurrency(value), name];
            }}
            labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px', color: 'var(--on-surface-variant)' }}
            iconType="circle"
          />
          <Bar 
            yAxisId="left"
            dataKey="currentAssets" 
            name={t('financials.charts.current_assets', 'Current Assets')} 
            fill="var(--primary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Bar 
            yAxisId="left"
            dataKey="currentLiabilities" 
            name={t('financials.charts.current_liabilities', 'Current Liabilities')} 
            fill="var(--tertiary)" 
            radius={[4, 4, 0, 0]} 
            maxBarSize={40}
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="currentRatio" 
            name={t('financials.charts.current_ratio', 'Current Ratio')} 
            stroke="var(--secondary)" 
            strokeWidth={2}
            dot={{ r: 4, fill: 'var(--surface)', strokeWidth: 2 }}
            activeDot={{ r: 6 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
