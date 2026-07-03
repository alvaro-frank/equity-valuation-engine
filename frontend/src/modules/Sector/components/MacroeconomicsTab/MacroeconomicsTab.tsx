import { useTranslation } from 'react-i18next';

import { MacroCard } from './components/MacroCard';

// --- Main Component ---

import type { SectorIndustrialValuationResult } from '@/common/types/valuation';

interface MacroeconomicsTabProps {
  sectorData: SectorIndustrialValuationResult;
}

export function MacroeconomicsTab({ sectorData }: MacroeconomicsTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in slide-in-from-bottom-4 duration-500 w-full">
      <MacroCard 
        bgIcon="trending_up" 
        icon="query_stats" 
        title={t('sector_view.economic_sensitivity')} 
        text={sectorData.economic_sensitivity} 
        sources={sectorData.sources}
      />
      <MacroCard 
        bgIcon="account_balance" 
        icon="percent" 
        title={t('sector_view.interest_rate')} 
        text={sectorData.interest_rate_exposure} 
        sources={sectorData.sources}
      />
    </div>
  );
}
