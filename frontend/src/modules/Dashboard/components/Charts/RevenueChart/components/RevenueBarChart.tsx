import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList,
} from 'recharts';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency, formatLargeNumber } from '@/common/utils/formatters';

export interface RevenueDataPoint {
  label: string;
  revenue: number;
  operatingIncome: number;
  netIncome: number;
  isTTM?: boolean;
}

interface RevenueBarChartProps {
  data: RevenueDataPoint[];
}

const formatLabel = (val: unknown) => {
  const num = Number(val);
  return (!isNaN(num) && num !== 0) ? formatLargeNumber(num) : '';
};

export function RevenueBarChart({ data }: RevenueBarChartProps) {
  const { t } = useTranslation();
  
  if (!data.length) {
    return (
      <div className="h-full flex items-center justify-center text-on-surface-variant">
        No data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="99%" height="100%" debounce={300}>
      <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--outline-variant)" vertical={false} />
        <XAxis 
          dataKey="label" 
          stroke="var(--outline)" 
          fontSize={11} 
          tickLine={false} 
          axisLine={false} 
          dy={10}
        />
        <YAxis 
          stroke="var(--outline)" 
          fontSize={11} 
          tickLine={false} 
          axisLine={false} 
          tickFormatter={(val) => formatLargeNumber(val)}
          domain={[0, (dataMax: number) => Math.ceil(dataMax * 1.1)]}
        />
        <Tooltip 
          cursor={{ fill: 'var(--surface-container-highest)' }}
          contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)' }}
          itemStyle={{ color: 'var(--on-surface)' }}
          formatter={(value: unknown, name: unknown) => [formatLargeCurrency(Number(value)), String(name)]}
          labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
        />
        <Legend 
          iconType="circle" 
          wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px' }}
        />
        <Bar dataKey="revenue" name={t('dashboard.revenue')} fill="var(--primary)" radius={[2, 2, 0, 0]}>
          <LabelList dataKey="revenue" position="top" fill="var(--outline)" fontSize={10} formatter={formatLabel} />
        </Bar>
        <Bar dataKey="operatingIncome" name={t('dashboard.operating_income')} fill="var(--secondary)" radius={[2, 2, 0, 0]}>
          <LabelList dataKey="operatingIncome" position="top" fill="var(--outline)" fontSize={10} formatter={formatLabel} />
        </Bar>
        <Bar dataKey="netIncome" name={t('dashboard.net_income')} fill="var(--tertiary)" radius={[2, 2, 0, 0]}>
          <LabelList dataKey="netIncome" position="top" fill="var(--outline)" fontSize={10} formatter={formatLabel} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
