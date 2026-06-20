import { useTranslation } from 'react-i18next';

import { CompetitiveForceCard } from './components/CompetitiveForceCard';

// --- Main Component ---

import type { SectorIndustrialValuationResult } from '@/common/types/valuation';

interface CompetitiveDynamicsTabProps {
  sectorData: SectorIndustrialValuationResult;
}

export function CompetitiveDynamicsTab({ sectorData }: CompetitiveDynamicsTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4 duration-500">
      <CompetitiveForceCard 
        icon="swords" 
        title={t('sector_view.rivalry')} 
        data={sectorData.rivalry_among_competitors} 
      />
      <CompetitiveForceCard 
        icon="shield" 
        title={t('sector_view.new_entrants')} 
        data={sectorData.threat_of_new_entrants} 
      />
      <CompetitiveForceCard 
        icon="hourglass_empty" 
        title={t('sector_view.obsolescence')} 
        data={sectorData.threat_of_obsolescence} 
      />
      <CompetitiveForceCard 
        icon="inventory" 
        title={t('sector_view.suppliers')} 
        data={sectorData.bargaining_power_of_suppliers} 
      />
      <CompetitiveForceCard 
        icon="shopping_cart" 
        title={t('sector_view.customers')} 
        data={sectorData.bargaining_power_of_customers} 
        className="md:col-span-2 lg:col-span-1" 
      />
    </div>
  );
}
