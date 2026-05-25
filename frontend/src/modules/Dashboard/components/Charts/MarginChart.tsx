import React, { useMemo, useState } from 'react';
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

interface MarginChartProps {
  quantData?: QuantitativeValuationResult;
}

export function MarginChart({ quantData }: MarginChartProps) {
  const [isQuarterly, setIsQuarterly] = useState(false);

  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const grossMarginSeries = quantData.metrics['gross_margin']?.yearly_data || [];
    const opMarginSeries = quantData.metrics['operating_margin']?.yearly_data || [];
    const netMarginSeries = quantData.metrics['net_margin']?.yearly_data || [];

    const sortedGross = [...grossMarginSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedGross.map((gmItem) => {
      const year = new Date(gmItem.date).getFullYear().toString();
      
      const opItem = opMarginSeries.find(
        (om) => new Date(om.date).getFullYear().toString() === year
      );
      
      const netItem = netMarginSeries.find(
        (nm) => new Date(nm.date).getFullYear().toString() === year
      );

      return {
        label: year,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
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
      
      const opItem = opMarginSeries.find((om) => om.date === gmItem.date);
      const netItem = netMarginSeries.find((nm) => nm.date === gmItem.date);

      return {
        label,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
      };
    });
  }, [quantData]);

  const formatPercent = (value: number) => `${value.toFixed(1)}%`;

  const renderChart = (data: any[]) => {
    if (!data.length) {
      return (
        <div className="h-full flex items-center justify-center text-on-surface-variant">
          No data available
        </div>
      );
    }

    return (
      <ResponsiveContainer width="99%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#32353c" vertical={false} />
          <XAxis 
            dataKey="label" 
            stroke="#8c909f" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            dy={5}
          />
          <YAxis 
            stroke="#8c909f" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            tickFormatter={(val) => `${val}%`}
          />
          <Tooltip 
            cursor={{ stroke: '#424754', strokeWidth: 1, strokeDasharray: '3 3' }}
            contentStyle={{ backgroundColor: '#10131a', borderColor: '#424754', color: '#e1e2ec' }}
            itemStyle={{ color: '#e1e2ec' }}
            formatter={(value: number, name: string) => [formatPercent(value), name]}
            labelStyle={{ color: '#8c909f', marginBottom: '4px' }}
          />
          <Legend 
            iconType="plainline" 
            wrapperStyle={{ fontSize: '11px', color: '#c2c6d6', paddingTop: '10px' }}
          />
          <Line 
            type="monotone" 
            dataKey="grossMargin" 
            name="GROSS MARGIN" 
            stroke="#2e7d32"
            strokeWidth={2}
            dot={{ r: 3, fill: '#2e7d32', strokeWidth: 0 }}
            activeDot={{ r: 5 }}
          />
          <Line 
            type="monotone" 
            dataKey="opMargin" 
            name="OPERATING MARGIN" 
            stroke="#ed6c02"
            strokeWidth={2}
            dot={{ r: 3, fill: '#ed6c02', strokeWidth: 0 }}
            activeDot={{ r: 5 }}
          />
          <Line 
            type="monotone" 
            dataKey="netMargin" 
            name="NET MARGIN" 
            stroke="#0288d1"
            strokeWidth={2}
            dot={{ r: 3, fill: '#0288d1', strokeWidth: 0 }}
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
        <div className="absolute inset-0 w-full h-full backface-hidden bg-surface-container-low border border-outline-variant flex flex-col" style={{ backfaceVisibility: 'hidden' }}>
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              Margin Evolution
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
              Quarterly Margin
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
