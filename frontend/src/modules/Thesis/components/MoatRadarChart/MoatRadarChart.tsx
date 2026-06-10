import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import type { MoatSources } from '../../../common/types/valuation';
import { useTranslation } from 'react-i18next';

export const MoatRadarChart: React.FC<{ data: MoatSources }> = ({ data }) => {
  const { t } = useTranslation();

  const chartData = [
    {
      subject: t('thesis_view.moat_sources.switching_costs'),
      score: data.switching_costs,
      fullMark: 5,
    },
    {
      subject: t('thesis_view.moat_sources.intangible_assets'),
      score: data.intangible_assets,
      fullMark: 5,
    },
    {
      subject: t('thesis_view.moat_sources.network_effect'),
      score: data.network_effect,
      fullMark: 5,
    },
    {
      subject: t('thesis_view.moat_sources.cost_advantage'),
      score: data.cost_advantage,
      fullMark: 5,
    },
    {
      subject: t('thesis_view.moat_sources.efficient_scale'),
      score: data.efficient_scale,
      fullMark: 5,
    },
  ];

  const renderCustomTick = (props: any) => {
    const { payload, x, y, textAnchor } = props;
    const words = payload.value.split(' ');
    
    let yOffset = 0;
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
      <text x={x} y={y + yOffset} textAnchor={textAnchor} fill="var(--on-surface-variant)" fontSize={10}>
        {words.map((word: string, index: number) => (
          <tspan x={x} dy={index === 0 ? 0 : 12} key={index}>
            {word}
          </tspan>
        ))}
      </text>
    );
  };

  return (
    <div className="w-full h-72 flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="60%" data={chartData}>
          <PolarGrid stroke="var(--on-surface-variant)" strokeOpacity={0.2} />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={renderCustomTick}
          />
          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1A1D20', borderColor: '#2D3135', color: '#E3E3E3', fontSize: '12px' }}
            itemStyle={{ color: '#F2C94C' }}
            formatter={(value) => [`${value} / 5`, 'Score']}
          />
          <Radar
            name="Moat Score"
            dataKey="score"
            stroke="#F2C94C"
            fill="#F2C94C"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
