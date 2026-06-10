import { SectorPerformanceChart } from '../SectorPerformanceChart';

interface MarketPerformanceTabProps {
  performanceData: any;
  isLoadingPerf: boolean;
}

export function MarketPerformanceTab({ performanceData, isLoadingPerf }: MarketPerformanceTabProps) {
  return (
    <div className="animate-in slide-in-from-bottom-4 duration-500 w-full">
      {isLoadingPerf ? (
        <div className="h-[400px] bg-surface-container-high rounded-xl animate-pulse"></div>
      ) : (
        <SectorPerformanceChart data={performanceData} />
      )}
    </div>
  );
}
