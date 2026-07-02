import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export interface ProjectedCashFlowsChartProps {
  cashflowData: { year: string; fcf: number }[];
}

export function ProjectedCashFlowsChart({ cashflowData }: ProjectedCashFlowsChartProps) {
  const formatBillion = (val: number) => `$${val.toFixed(1)}B`;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={cashflowData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--outline-variant)" />
        <XAxis dataKey="year" stroke="var(--on-surface)" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis tickFormatter={formatBillion} stroke="var(--on-surface)" fontSize={12} tickLine={false} axisLine={false} />
        <Tooltip 
          cursor={{fill: 'var(--surface-container-highest)', opacity: 0.4}}
          contentStyle={{ backgroundColor: 'var(--surface-container-high)', border: '1px solid var(--outline-variant)', borderRadius: '8px' }}
          itemStyle={{ color: 'var(--on-surface)', fontWeight: 'bold' }}
          labelStyle={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}
          formatter={(value: any) => [formatBillion(value as number), 'FCF']}
        />
        <Bar dataKey="fcf" fill="var(--tertiary)" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
