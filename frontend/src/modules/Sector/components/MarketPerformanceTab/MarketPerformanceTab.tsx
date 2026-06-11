import { SectorPerformanceChart } from '../SectorPerformanceChart';

// --- Sub-Components (Rule 2.23) ---

function MarketPerformanceSkeleton() {
  return (
    <div className="animate-in slide-in-from-bottom-4 duration-500 w-full">
      <div className="h-[400px] bg-surface-container-high rounded-xl animate-pulse"></div>
    </div>
  );
}

// --- Main Component ---

interface MarketPerformanceTabProps {
  performanceData: unknown;
  isLoadingPerf: boolean;
}

export function MarketPerformanceTab({ performanceData, isLoadingPerf }: MarketPerformanceTabProps) {
  if (isLoadingPerf) {
    return <MarketPerformanceSkeleton />;
  }

  return (
    <div className="animate-in slide-in-from-bottom-4 duration-500 w-full">
      <SectorPerformanceChart data={performanceData} />
    </div>
  );
}
