import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { QuantitativeValuationResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

// --- Types ---
interface MarginDataPoint {
  label: string;
  grossMargin: number;
  opMargin: number | null;
  netMargin: number | null;
  isTTM?: boolean;
}

interface MarginChartProps {
  quantData?: QuantitativeValuationResult;
}

import { formatPercentage } from '@/common/utils/formatters';

// --- Custom Hooks (Rule 1.11, 2.39) ---
import { useMarginChartData } from './useMarginChartData';

// --- Sub-Components (Rule 2.23, 2.31, 2.41) ---
function MarginLineChart({ data }: { data: MarginDataPoint[] }) {
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
      <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--outline-variant)" vertical={false} />
        <XAxis 
          dataKey="label" 
          stroke="var(--outline)" 
          fontSize={11} 
          tickLine={false} 
          axisLine={false} 
          dy={5}
        />
        <YAxis 
          stroke="var(--outline)" 
          fontSize={11} 
          tickLine={false} 
          axisLine={false} 
          tickFormatter={(val) => `${val}%`}
        />
        <Tooltip 
          cursor={{ stroke: 'var(--outline-variant)', strokeWidth: 1, strokeDasharray: '3 3' }}
          contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)' }}
          itemStyle={{ color: 'var(--on-surface)' }}
          formatter={(value: unknown, name: unknown) => [formatPercentage(Number(value)), String(name)]}
          labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
        />
        <Legend 
          iconType="plainline" 
          wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px' }}
        />
        <Line 
          type="monotone" 
          dataKey="grossMargin" 
          name={t('dashboard.gross_margin')} 
          stroke="var(--primary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--primary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
        <Line 
          type="monotone" 
          dataKey="opMargin" 
          name={t('dashboard.operating_margin')} 
          stroke="var(--secondary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--secondary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
        <Line 
          type="monotone" 
          dataKey="netMargin" 
          name={t('dashboard.net_margin', 'NET MARGIN')} 
          stroke="var(--tertiary)"
          strokeWidth={2}
          dot={{ r: 3, fill: 'var(--tertiary)', strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

interface ChartCardFaceProps {
  title: string;
  actionText: string;
  onAction: () => void;
  data: MarginDataPoint[];
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
        <MarginLineChart data={data} />
      </div>
    </div>
  );
}

// --- Main Component ---
export function MarginChart({ quantData }: MarginChartProps) {
  const { t } = useTranslation();
  const [isQuarterly, setIsQuarterly] = useState(false);
  const { annualData, quarterlyData } = useMarginChartData(quantData);

  return (
    <div className="bg-transparent h-[400px]" style={{ perspective: '1000px' }}>
      <div 
        className="w-full h-full relative transition-all duration-700" 
        style={{ transformStyle: 'preserve-3d', transform: isQuarterly ? 'rotateY(180deg)' : 'rotateY(0)' }}
      >
        <ChartCardFace 
          title={t('dashboard.margin_chart_annual')}
          actionText={t('dashboard.show_quarters')}
          onAction={() => setIsQuarterly(true)}
          data={annualData}
        />
        <ChartCardFace 
          title={t('dashboard.margin_chart_quarterly')}
          actionText={t('dashboard.show_annual')}
          onAction={() => setIsQuarterly(false)}
          data={quarterlyData}
          isBackFace
        />
      </div>
    </div>
  );
}
