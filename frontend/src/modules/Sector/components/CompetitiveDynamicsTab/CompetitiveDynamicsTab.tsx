import { useTranslation } from 'react-i18next';

// --- Sub-Components (Rule 2.21, 2.41) ---

interface CompetitiveForceCardProps {
  icon: string;
  title: string;
  data: Record<string, string>;
  className?: string;
}

function CompetitiveForceCard({ icon, title, data, className = '' }: CompetitiveForceCardProps) {
  if (!data) return null;
  
  return (
    <div className={`bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4 ${className}`}>
      <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
        <span className="material-symbols-outlined text-primary text-[28px]">{icon}</span>
        <h3 className="font-display-sm text-xl text-on-surface">{title}</h3>
      </div>
      <div className="space-y-4">
        {Object.entries(data).map(([factor, analysis]) => (
          <div key={factor}>
            <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
            <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

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
