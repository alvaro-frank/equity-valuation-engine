import { useState } from 'react';
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
import type { QuantitativeValuationResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency, formatLargeNumber } from '@/common/utils/formatters';

// --- Types ---
interface RevenueDataPoint {
  label: string;
  revenue: number;
  operatingIncome: number;
  netIncome: number;
  isTTM?: boolean;
}

interface RevenueChartProps {
  quantData?: QuantitativeValuationResult;
}

// --- Helper Functions (Rule 2.22) ---
const formatLabel = (val: unknown) => {
  const num = Number(val);
  return (!isNaN(num) && num !== 0) ? formatLargeNumber(num) : '';
};

import { useRevenueChartData } from './useRevenueChartData';

// --- Sub-Components (Rule 2.23, 2.31, 2.41) ---
function RevenueBarChart({ data }: { data: RevenueDataPoint[] }) {
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

interface ChartCardFaceProps {
  title: string;
  actionText: string;
  onAction: () => void;
  data: RevenueDataPoint[];
  isBackFace?: boolean;
}

function ChartCardFace({ title, actionText, onAction, data, isBackFace = false }: ChartCardFaceProps) {
  return (
    <div 
      className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden" 
      style={{ backfaceVisibility: 'hidden', transform: isBackFace ? 'rotateY(180deg)' : 'none' }}
    >
      <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {title}
        </h3>
        <button 
          onClick={onAction}
          className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
        >
          {actionText}
        </button>
      </div>
      <div className="p-4 flex-1 min-h-0 min-w-0">
        <RevenueBarChart data={data} />
      </div>
    </div>
  );
}

// --- Main Component ---
export function RevenueChart({ quantData }: RevenueChartProps) {
  const { t } = useTranslation();
  const [isQuarterly, setIsQuarterly] = useState(false);
  const { annualData, quarterlyData } = useRevenueChartData(quantData);

  return (
    <div className="bg-transparent h-[400px]" style={{ perspective: '1000px' }}>
      <div 
        className="w-full h-full relative transition-all duration-700" 
        style={{ transformStyle: 'preserve-3d', transform: isQuarterly ? 'rotateY(180deg)' : 'rotateY(0)' }}
      >
        <ChartCardFace 
          title={t('dashboard.revenue_chart_annual')}
          actionText={t('dashboard.show_quarters')}
          onAction={() => setIsQuarterly(true)}
          data={annualData}
        />
        <ChartCardFace 
          title={t('dashboard.revenue_chart_quarterly')}
          actionText={t('dashboard.show_annual')}
          onAction={() => setIsQuarterly(false)}
          data={quarterlyData}
          isBackFace
        />
      </div>
    </div>
  );
}
