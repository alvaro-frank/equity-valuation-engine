import { useMemo, useState } from 'react';
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
import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

interface RevenueDataPoint {
  label: string;
  revenue: number;
  operatingIncome: number;
  netIncome: number;
}

interface RevenueChartProps {
  quantData?: QuantitativeValuationResult;
}

export function RevenueChart({ quantData }: RevenueChartProps) {
  const { t } = useTranslation();
  const [isQuarterly, setIsQuarterly] = useState(false);

  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const revenueSeries = quantData.metrics['revenue']?.yearly_data || [];
    const opIncomeSeries = quantData.metrics['operating_income']?.yearly_data || [];
    const netIncomeSeries = quantData.metrics['net_income']?.yearly_data || [];

    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedRevenue.map((revItem) => {
      const year = new Date(revItem.date).getFullYear().toString();
      const opIncomeItem = opIncomeSeries.find(
        (oi) => new Date(oi.date).getFullYear().toString() === year
      );
      const netIncomeItem = netIncomeSeries.find(
        (ni) => new Date(ni.date).getFullYear().toString() === year
      );

      return {
        label: year,
        revenue: Number(revItem.value) / 1e9,
        operatingIncome: opIncomeItem ? Number(opIncomeItem.value) / 1e9 : 0,
        netIncome: netIncomeItem ? Number(netIncomeItem.value) / 1e9 : 0,
      };
    });
  }, [quantData]);

  const quarterlyData = useMemo(() => {
    if (!quantData || !quantData.quarterly_metrics) return [];

    const revenueSeries = quantData.quarterly_metrics['revenue'] || [];
    const opIncomeSeries = quantData.quarterly_metrics['operating_income'] || [];
    const netIncomeSeries = quantData.quarterly_metrics['net_income'] || [];

    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedRevenue.map((revItem) => {
      // Format as Q1 24, Q2 24
      const d = new Date(revItem.date);
      const q = Math.ceil((d.getMonth() + 1) / 3);
      const yy = d.getFullYear().toString().slice(2);
      const label = `Q${q} ${yy}`;
      
      const opIncomeItem = opIncomeSeries.find((oi: BaseMetric) => oi.date === revItem.date);
      const netIncomeItem = netIncomeSeries.find((ni: BaseMetric) => ni.date === revItem.date);

      return {
        label,
        revenue: Number(revItem.value) / 1e9,
        operatingIncome: opIncomeItem ? Number(opIncomeItem.value) / 1e9 : 0,
        netIncome: netIncomeItem ? Number(netIncomeItem.value) / 1e9 : 0,
      };
    });
  }, [quantData]);

  // Custom formatter for the tooltip
  const formatCurrency = (value: number) => `$${value.toFixed(1)}B`;

  const renderChart = (data: RevenueDataPoint[]) => {
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
            tickFormatter={(val) => `${val}B`}
            domain={[0, (dataMax: number) => Math.ceil(dataMax * 1.1)]}
          />
          <Tooltip 
            cursor={{ fill: 'var(--surface-container-highest)' }}
            contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)' }}
            itemStyle={{ color: 'var(--on-surface)' }}
            formatter={(value: unknown, name: unknown) => [formatCurrency(Number(value)), String(name)]}
            labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
          />
          <Legend 
            iconType="circle" 
            wrapperStyle={{ fontSize: '11px', color: 'var(--on-surface-variant)', paddingTop: '10px' }}
          />
          <Bar dataKey="revenue" name={t('dashboard.revenue')} fill="var(--primary)" radius={[2, 2, 0, 0]}>
            <LabelList dataKey="revenue" position="top" fill="var(--outline)" fontSize={10} formatter={(val: unknown) => { const num = Number(val); return (!isNaN(num) && num !== 0) ? num.toFixed(1) + 'B' : ''; }} />
          </Bar>
          <Bar dataKey="operatingIncome" name={t('dashboard.operating_income')} fill="var(--secondary)" radius={[2, 2, 0, 0]}>
            <LabelList dataKey="operatingIncome" position="top" fill="var(--outline)" fontSize={10} formatter={(val: unknown) => { const num = Number(val); return (!isNaN(num) && num !== 0) ? num.toFixed(1) + 'B' : ''; }} />
          </Bar>
          <Bar dataKey="netIncome" name={t('dashboard.net_income')} fill="var(--tertiary)" radius={[2, 2, 0, 0]}>
            <LabelList dataKey="netIncome" position="top" fill="var(--outline)" fontSize={10} formatter={(val: unknown) => { const num = Number(val); return (!isNaN(num) && num !== 0) ? num.toFixed(1) + 'B' : ''; }} />
          </Bar>
        </BarChart>
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
              {t('dashboard.revenue_chart_annual')}
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
              {t('dashboard.revenue_chart_quarterly')}
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
