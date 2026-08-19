import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import type { MoatSources } from '@/common/types/valuation';
import { useMoatRadarChart } from './useMoatRadarChart';

// --- Sub-Components (Rule 2.23) ---

interface CustomTickProps {
  payload: { value: string; index: number };
  x: number | string;
  y: number | string;
  textAnchor: "inherit" | "end" | "middle" | "start" | undefined;
}

function CustomTick(props: CustomTickProps) {
  const { payload, x, y, textAnchor } = props;
  const words = payload.value.split(' ');
  
  let yOffset;
  if (payload.index === 0) {
    // Top label: shift UP so all lines are above the point
    yOffset = -((words.length - 1) * 12) - 5;
  } else if (payload.index === 2 || payload.index === 3) {
    // Bottom labels: shift DOWN so they start below the point
    yOffset = 12;
  } else {
    // Side labels: center vertically
    yOffset = -((words.length - 1) * 6);
  }

  return (
    <text x={x} y={Number(y) + yOffset} textAnchor={textAnchor} fill="var(--on-surface-variant)" fontSize={10}>
      {words.map((word: string, index: number) => (
        <tspan x={x} dy={index === 0 ? 0 : 12} key={index}>
          {word}
        </tspan>
      ))}
    </text>
  );
}

// --- Main Component (Rule 2.18) ---

interface MoatRadarChartProps {
  data: MoatSources;
}

export function MoatRadarChart({ data }: MoatRadarChartProps) {
  const chartData = useMoatRadarChart(data);

  return (
    <div className="w-full h-72 flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="60%" data={chartData}>
          <PolarGrid stroke="var(--on-surface-variant)" strokeOpacity={0.2} />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={CustomTick}
          />
          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'var(--surface-container-high)', borderColor: 'var(--outline-variant)', color: 'var(--on-surface)', fontSize: '12px' }}
            itemStyle={{ color: 'var(--primary)' }}
            formatter={(value) => [`${value} / 5`, 'Score']}
          />
          <Radar
            name="Moat Score"
            dataKey="score"
            stroke="var(--primary)"
            fill="var(--primary)"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
