import { SectorPerformanceChart } from '../SectorPerformanceChart';

import { MarketPerformanceSkeleton } from './components/MarketPerformanceSkeleton';

// --- Main Component ---

import type { SectorPerformanceData } from '@/common/types/valuation';

interface MarketPerformanceTabProps {
  performanceData: SectorPerformanceData | undefined;
  isLoadingPerf: boolean;
  companyName?: string;
}

export function MarketPerformanceTab({ performanceData, isLoadingPerf, companyName }: MarketPerformanceTabProps) {
  if (isLoadingPerf) {
    return <MarketPerformanceSkeleton />;
  }

  return (
    <div className="animate-in slide-in-from-bottom-4 duration-500 w-full">
      <SectorPerformanceChart data={performanceData} companyName={companyName} />
    </div>
  );
}
