import { RevenueChart } from '@/modules/Dashboard/components/Charts/RevenueChart';
import { MarginChart } from '@/modules/Dashboard/components/Charts/MarginChart';
import { DashboardHeader } from './components/DashboardHeader/index';
import { KPIGrid } from './components/KPIGrid/index';
import { BusinessMoatPanel } from './components/BusinessMoatPanel/index';
import { LeadershipPanel } from './components/LeadershipPanel/index';
import { useDashboardData } from './hooks/useDashboardData';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';

interface DashboardViewProps {
  ticker: string;
  quantData?: QuantitativeValuationResult;
  qualData?: QualitativeValuationResult;
  onSearch?: (ticker: string) => void;
}

export function DashboardView({ ticker, quantData, qualData, onSearch }: DashboardViewProps) {
  const { 
    getLatestMetric, 
    getRawLatestMetric, 
    ev, 
    fcf, 
    ceoViewModel 
  } = useDashboardData({ quantData, qualData });

  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap">
      <DashboardHeader 
        ticker={ticker} 
        quantData={quantData} 
        qualData={qualData} 
        onSearch={onSearch} 
      />

      <KPIGrid 
        quantData={quantData} 
        ev={ev} 
        fcf={fcf} 
        getLatestMetric={getLatestMetric} 
        getRawLatestMetric={getRawLatestMetric} 
      />

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
        <BusinessMoatPanel qualData={qualData} />
        <LeadershipPanel qualData={qualData} ceoViewModel={ceoViewModel} />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-panel-gap">
        <RevenueChart quantData={quantData} />
        <MarginChart quantData={quantData} />
      </section>
    </div>
  );
}
