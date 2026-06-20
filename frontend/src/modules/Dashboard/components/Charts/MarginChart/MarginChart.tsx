import { useState } from 'react';
import type { QuantitativeValuationResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { useMarginChartData } from './useMarginChartData';
import { ChartCardFace } from '../components/ChartCardFace';
import { MarginLineChart } from './components';

interface MarginChartProps {
  quantData?: QuantitativeValuationResult;
}

export function MarginChart({ quantData }: MarginChartProps) {
  const { t } = useTranslation();
  const [isQuarterly, setIsQuarterly] = useState(false);
  const [hasFlipped, setHasFlipped] = useState(false);
  const { annualData, quarterlyData } = useMarginChartData(quantData);

  const handleShowQuarterly = () => { setIsQuarterly(true); setHasFlipped(true); };
  const handleShowAnnual = () => setIsQuarterly(false);

  return (
    <div className="bg-transparent h-[400px]" style={{ perspective: '1000px' }}>
      <div 
        className="w-full h-full relative transition-all duration-700" 
        style={{ transformStyle: 'preserve-3d', transform: isQuarterly ? 'rotateY(180deg)' : 'rotateY(0)' }}
      >
        <ChartCardFace 
          title={t('dashboard.margin_chart_annual')}
          actionText={t('dashboard.show_quarters')}
          onAction={handleShowQuarterly}
        >
          <MarginLineChart data={annualData} />
        </ChartCardFace>
        
        {hasFlipped && (
          <ChartCardFace 
            title={t('dashboard.margin_chart_quarterly')}
            actionText={t('dashboard.show_annual')}
            onAction={handleShowAnnual}
            isBackFace
          >
            <MarginLineChart data={quarterlyData} />
          </ChartCardFace>
        )}
      </div>
    </div>
  );
}
