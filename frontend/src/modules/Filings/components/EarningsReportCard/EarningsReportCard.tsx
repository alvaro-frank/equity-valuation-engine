import type { EarningsReportResult } from '@/common/types/valuation';
import {
  CorePerformanceGrid,
  CapitalAllocationPanel,
  RiskDeconstructionPanel,
  TextualAnalysisPanel,
  BottomLinePanel
} from './components';

// --- Main Component ---

interface EarningsReportCardProps {
  data: EarningsReportResult;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  quantData?: any;
}

export function EarningsReportCard({ data, quantData }: EarningsReportCardProps) {
  const { core_performance, capital_allocation, risk_deconstruction, sources } = data;

  return (
    <div className="space-y-6 mt-6 animate-fade-in">
      <CorePerformanceGrid data={core_performance} quantData={quantData} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CapitalAllocationPanel data={capital_allocation} sources={sources} />
        <RiskDeconstructionPanel data={risk_deconstruction} sources={sources} />
      </div>

      <TextualAnalysisPanel 
        forwardGuidance={data.forward_guidance} 
        moatTrajectory={data.moat_trajectory} 
        sources={sources}
      />

      <BottomLinePanel text={data.bottom_line} sources={sources} />
    </div>
  );
}
