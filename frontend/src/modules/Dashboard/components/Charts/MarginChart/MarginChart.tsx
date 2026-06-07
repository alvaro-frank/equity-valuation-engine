import { useMemo, useState } from 'react';
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
import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

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

export function MarginChart({ quantData }: MarginChartProps) {
  const { t } = useTranslation();
  const [isQuarterly, setIsQuarterly] = useState(false);

  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const grossMarginSeries = quantData.metrics['gross_margin']?.yearly_data || [];
    const opMarginSeries = quantData.metrics['operating_margin']?.yearly_data || [];
    const netMarginSeries = quantData.metrics['net_margin']?.yearly_data || [];

    const sortedGross = [...grossMarginSeries].sort(
      (a, b) => {
        if (a.date === 'TTM') return 1;
        if (b.date === 'TTM') return -1;
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      }
    );

    return sortedGross.map((gmItem) => {
      const isTTM = gmItem.date === 'TTM';
      const year = isTTM ? 'TTM' : new Date(gmItem.date).getFullYear().toString();
      
      const opItem = opMarginSeries.find(
        (om) => om.date === gmItem.date || new Date(om.date).getFullYear().toString() === year
      );
      
      const netItem = netMarginSeries.find(
        (nm) => nm.date === gmItem.date || new Date(nm.date).getFullYear().toString() === year
      );

      return {
        label: year,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
        isTTM,
      };
    });
  }, [quantData]);

  const quarterlyData = useMemo(() => {
    if (!quantData || !quantData.quarterly_metrics) return [];

    const grossMarginSeries = quantData.quarterly_metrics['gross_margin'] || [];
    const opMarginSeries = quantData.quarterly_metrics['operating_margin'] || [];
    const netMarginSeries = quantData.quarterly_metrics['net_margin'] || [];

    const sortedGross = [...grossMarginSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedGross.map((gmItem) => {
      const d = new Date(gmItem.date);
      const q = Math.ceil((d.getMonth() + 1) / 3);
      const yy = d.getFullYear().toString().slice(2);
      const label = `Q${q} ${yy}`;
      
      const opItem = opMarginSeries.find((om: BaseMetric) => om.date === gmItem.date);
      const netItem = netMarginSeries.find((nm: BaseMetric) => nm.date === gmItem.date);

      return {
        label,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
      };
    });
  }, [quantData]);

  const formatPercent = (value: number) => `${value.toFixed(1)}%`;

  const renderChart = (data: MarginDataPoint[]) => {
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
            formatter={(value: unknown, name: unknown) => [formatPercent(Number(value)), String(name)]}
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
  };

  return (
    <div className="bg-transparent h-[400px]" style={{ perspective: '1000px' }}>
      <div 
        className="w-full h-full relative transition-all duration-700" 
        style={{ transformStyle: 'preserve-3d', transform: isQuarterly ? 'rotateY(180deg)' : 'rotateY(0)' }}
      >
        {/* Front Face: Annual */}
        <div className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden" style={{ backfaceVisibility: 'hidden' }}>
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              {t('dashboard.margin_chart_annual')}
            </h3>
            <button 
              onClick={() => setIsQuarterly(true)}
              className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
            >
              {t('dashboard.show_quarters')}
            </button>
          </div>
          <div className="p-4 flex-1 min-h-0 min-w-0">
            {renderChart(annualData)}
          </div>
        </div>

        {/* Back Face: Quarterly */}
        <div className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden" style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              {t('dashboard.margin_chart_quarterly')}
            </h3>
            <button 
              onClick={() => setIsQuarterly(false)}
              className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
            >
              {t('dashboard.show_annual')}
            </button>
          </div>
          <div className="p-4 flex-1 min-h-0 min-w-0">
            {renderChart(quarterlyData)}
          </div>
        </div>
      </div>
    </div>
  );
}
