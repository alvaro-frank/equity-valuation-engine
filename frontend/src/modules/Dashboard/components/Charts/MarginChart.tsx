import React, { useMemo } from 'react';
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
  const chartData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const grossMarginSeries = quantData.metrics['gross_margin']?.yearly_data || [];
    const opMarginSeries = quantData.metrics['operating_margin']?.yearly_data || [];
    const netMarginSeries = quantData.metrics['net_margin']?.yearly_data || [];

    // Sort by date ascending
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
        year,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
      };
    });
  }, [quantData]);

  if (!chartData.length) {
    return (
      <div className="h-full flex items-center justify-center text-on-surface-variant">
        No data available
      </div>
    );
  }

  const formatPercent = (value: number) => `${value.toFixed(1)}%`;

  return (
    <div className="bg-surface-container-low border border-outline-variant flex flex-col h-[400px]">
      <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
        <div>
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
            Margin Evolution
          </h3>
        </div>
      </div>
      <div className="p-4 flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#32353c" vertical={false} />
            <XAxis 
              dataKey="year" 
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
              tickFormatter={(val) => `${val}%`}
            />
            <Tooltip 
              cursor={{ stroke: '#424754', strokeWidth: 1, strokeDasharray: '3 3' }}
              contentStyle={{ backgroundColor: '#10131a', borderColor: '#424754', color: '#e1e2ec' }}
              itemStyle={{ color: '#e1e2ec' }}
              formatter={(value: number) => [formatPercent(value), '']}
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
              stroke="#2e7d32" // Using a green color for gross
              strokeWidth={2}
              dot={{ r: 3, fill: '#2e7d32', strokeWidth: 0 }}
              activeDot={{ r: 5 }}
            />
            <Line 
              type="monotone" 
              dataKey="opMargin" 
              name="OPERATING MARGIN" 
              stroke="#ed6c02" // Using an orange color for operating
              strokeWidth={2}
              dot={{ r: 3, fill: '#ed6c02', strokeWidth: 0 }}
              activeDot={{ r: 5 }}
            />
            <Line 
              type="monotone" 
              dataKey="netMargin" 
              name="NET MARGIN" 
              stroke="#0288d1" // Using a blue color for net
              strokeWidth={2}
              dot={{ r: 3, fill: '#0288d1', strokeWidth: 0 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
