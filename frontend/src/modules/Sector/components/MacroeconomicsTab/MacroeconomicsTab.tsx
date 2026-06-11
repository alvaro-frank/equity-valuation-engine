import { useTranslation } from 'react-i18next';

// --- Sub-Components (Rule 2.21, 2.41) ---

interface MacroCardProps {
  bgIcon: string;
  icon: string;
  title: string;
  text: string;
}

function MacroCard({ bgIcon, icon, title, text }: MacroCardProps) {
  if (!text) return null;
  
  return (
    <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-8 opacity-5">
        <span className="material-symbols-outlined text-[120px]">{bgIcon}</span>
      </div>
      <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
        <span className="material-symbols-outlined text-primary text-[32px]">{icon}</span>
        <h3 className="font-display-sm text-2xl text-on-surface">{title}</h3>
      </div>
      <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
        {text}
      </p>
    </div>
  );
}

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
      />
      <MacroCard 
        bgIcon="account_balance" 
        icon="percent" 
        title={t('sector_view.interest_rate')} 
        text={sectorData.interest_rate_exposure} 
      />
    </div>
  );
}
