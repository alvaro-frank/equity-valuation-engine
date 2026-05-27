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
} from 'recharts';
import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';

interface RevenueDataPoint {
  label: string;
  revenue: number;
  netIncome: number;
}

interface RevenueChartProps {
  quantData?: QuantitativeValuationResult;
}

export function RevenueChart({ quantData }: RevenueChartProps) {
  const [isQuarterly, setIsQuarterly] = useState(false);

  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const revenueSeries = quantData.metrics['revenue']?.yearly_data || [];
    const netIncomeSeries = quantData.metrics['net_income']?.yearly_data || [];

    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedRevenue.map((revItem) => {
      const year = new Date(revItem.date).getFullYear().toString();
      const netIncomeItem = netIncomeSeries.find(
        (ni) => new Date(ni.date).getFullYear().toString() === year
      );

      return {
        label: year,
        revenue: Number(revItem.value) / 1e9,
        netIncome: netIncomeItem ? Number(netIncomeItem.value) / 1e9 : 0,
      };
    });
  }, [quantData]);

  const quarterlyData = useMemo(() => {
    if (!quantData || !quantData.quarterly_metrics) return [];

    const revenueSeries = quantData.quarterly_metrics['revenue'] || [];
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
      
      const netIncomeItem = netIncomeSeries.find((ni: BaseMetric) => ni.date === revItem.date);

      return {
        label,
        revenue: Number(revItem.value) / 1e9,
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
      <ResponsiveContainer width="99%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#32353c" vertical={false} />
          <XAxis 
            dataKey="label" 
            stroke="#8c909f" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            dy={10}
          />
          <YAxis 
            stroke="#8c909f" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            tickFormatter={(val) => `${val}B`}
          />
          <Tooltip 
            cursor={{ fill: '#272a31' }}
            contentStyle={{ backgroundColor: '#10131a', borderColor: '#424754', color: '#e1e2ec' }}
            itemStyle={{ color: '#e1e2ec' }}
            formatter={(value: number | string | Array<number | string>, name: string | number) => [formatCurrency(Number(value)), String(name)]}
            labelStyle={{ color: '#8c909f', marginBottom: '4px' }}
          />
          <Legend 
            iconType="circle" 
            wrapperStyle={{ fontSize: '11px', color: '#c2c6d6', paddingTop: '10px' }}
          />
          <Bar dataKey="revenue" name="REVENUE" fill="#4d8eff" radius={[2, 2, 0, 0]} />
          <Bar dataKey="netIncome" name="NET INCOME" fill="#a9bad3" radius={[2, 2, 0, 0]} />
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
        <div className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col" style={{ backfaceVisibility: 'hidden' }}>
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              Annual Revenue vs Net Income
            </h3>
            <button 
              onClick={() => setIsQuarterly(true)}
              className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
            >
              Show Quarters
            </button>
          </div>
          <div className="p-4 flex-1 min-h-0 min-w-0">
            {renderChart(annualData)}
          </div>
        </div>

        {/* Back Face: Quarterly */}
        <div className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col" style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              Quarterly Revenue vs Net Income
            </h3>
            <button 
              onClick={() => setIsQuarterly(false)}
              className="text-xs px-2 py-1 bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant rounded transition-colors"
            >
              Show Annual
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
