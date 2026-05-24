import React, { useMemo } from 'react';
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
import type { QuantitativeValuationResult } from '@/common/types/valuation';

interface RevenueChartProps {
  quantData?: QuantitativeValuationResult;
}

export function RevenueChart({ quantData }: RevenueChartProps) {
  const chartData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const revenueSeries = quantData.metrics['revenue']?.yearly_data || [];
    const netIncomeSeries = quantData.metrics['net_income']?.yearly_data || [];

    // Assuming both series have the same dates, we can map over one of them
    // and extract the year from the date string (e.g. '2023-12-31' -> '2023')
    
    // Sort by date ascending for the chart (left to right = oldest to newest)
    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedRevenue.map((revItem) => {
      const year = new Date(revItem.date).getFullYear().toString();
      const netIncomeItem = netIncomeSeries.find(
        (ni) => new Date(ni.date).getFullYear().toString() === year
      );

      return {
        year,
        revenue: Number(revItem.value) / 1e9, // Convert to Billions for readability
        netIncome: netIncomeItem ? Number(netIncomeItem.value) / 1e9 : 0,
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

  // Custom formatter for the tooltip
  const formatCurrency = (value: number) => `$${value.toFixed(1)}B`;

  return (
    <div className="bg-surface-container-low border border-outline-variant flex flex-col h-[400px]">
      <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
        <div>
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
            Revenue vs Net Income
          </h3>
        </div>
      </div>
      <div className="p-4 flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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
              tickFormatter={(val) => `${val}B`}
            />
            <Tooltip 
              cursor={{ fill: '#272a31' }}
              contentStyle={{ backgroundColor: '#10131a', borderColor: '#424754', color: '#e1e2ec' }}
              itemStyle={{ color: '#e1e2ec' }}
              formatter={(value: number) => [formatCurrency(value), '']}
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
      </div>
    </div>
  );
}
