import { ExecutivesSection } from './components/ExecutivesSection';
import { ShareholdersSection } from './components/ShareholdersSection';
import { LeadershipInsights } from './components/LeadershipInsights';
import { CapitalAllocationStrategy } from './components/CapitalAllocationStrategy';
import type { QualitativeValuationResult } from '@/common/types/valuation';

interface LeadershipTabProps {
  qualData: QualitativeValuationResult;
}

export function LeadershipTab({ qualData }: LeadershipTabProps) {
  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="space-y-8 lg:col-span-2">
          <LeadershipInsights content={qualData.management_insights} />
          {qualData.capital_allocation_strategy && (
            <CapitalAllocationStrategy content={qualData.capital_allocation_strategy} />
          )}
        </div>
        
        <div className="space-y-8 lg:border-l lg:border-outline-variant/50 lg:pl-8">
          <ExecutivesSection executives={qualData.key_executives} />
          
          <div className="w-full h-px bg-gradient-to-r from-transparent via-outline-variant/50 to-transparent my-2" />
          
          <ShareholdersSection shareholders={qualData.major_shareholders || {}} />
        </div>
      </div>
    </div>
  );
}
