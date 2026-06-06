import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip } from 'recharts';
import type { MoatSources } from '../../../common/types/valuation';
import { useTranslation } from 'react-i18next';

interface MoatRadarChartProps {
  data: MoatSources;
}

export const MoatRadarChart: React.FC<MoatRadarChartProps> = ({ data }) => {
  const { t } = useTranslation();

  const chartData = [
    {
      subject: t('thesis_view.moat_sources.intangible_assets'),
      score: data.intangible_assets,
      fullMark: 5,
    },
    {
      subject: t('thesis_view.moat_sources.switching_costs'),
      score: data.switching_costs,
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

  return (
    <div className="w-full h-64 flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
          <PolarGrid stroke="rgba(255, 255, 255, 0.1)" />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: '#A3A3A3', fontSize: 10 }}
          />
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
