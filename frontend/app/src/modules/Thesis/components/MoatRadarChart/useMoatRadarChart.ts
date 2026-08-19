import { useMemo } from 'react';
import type { MoatSources } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

export function useMoatRadarChart(data: MoatSources) {
  const { t } = useTranslation();

  const chartData = useMemo(() => [
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
  ], [data, t]);

  return chartData;
}
