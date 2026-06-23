import { MoatOverview } from './components/MoatOverview';
import { MoatTrajectory } from './components/MoatTrajectory';
import { CompetitorsList } from './components/CompetitorsList';
import type { QualitativeValuationResult } from '@/common/types/valuation';

interface MoatTabProps {
  qualData: QualitativeValuationResult;
}

export function MoatTab({ qualData }: MoatTabProps) {
  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <MoatOverview content={qualData.competitive_advantage} moatSources={qualData.moat_sources} />
          <MoatTrajectory 
            status={qualData.moat_trajectory_status} 
            description={qualData.moat_trajectory_description} 
          />
        </div>
        <CompetitorsList competitors={qualData.competitors || []} />
      </div>
    </div>
  );
}
