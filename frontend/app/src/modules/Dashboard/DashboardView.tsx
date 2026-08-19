import { RevenueChart } from '@/modules/Dashboard/components/Charts/RevenueChart';
import { MarginChart } from '@/modules/Dashboard/components/Charts/MarginChart';
import { DashboardHeader } from './components/DashboardHeader/index';
import { KPIGrid } from './components/KPIGrid/index';
import { BusinessMoatPanel } from './components/BusinessMoatPanel/index';
import { LeadershipPanel } from './components/LeadershipPanel/index';
import { useDashboardData } from './hooks/useDashboardData';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';
import { SourcesProvider } from '@/common/contexts/SourcesContext';

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
    <SourcesProvider sources={qualData?.sources}>
      <div className="max-w-[1600px] mx-auto w-full flex-1 flex flex-col pb-12">
        
        {/* Sticky Header with Blur */}
        <div className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 pt-6 pb-4 flex flex-col gap-6 -mx-4 px-4 sm:-mx-8 sm:px-8 border-b border-outline-variant/20 mb-6">
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
        </div>

        {/* Scrollable Content */}
        <div className="flex flex-col gap-panel-gap">

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
          <BusinessMoatPanel qualData={qualData} />
          <LeadershipPanel qualData={qualData} ceoViewModel={ceoViewModel} />
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-2 gap-panel-gap">
          <RevenueChart quantData={quantData} />
          <MarginChart quantData={quantData} />
        </section>
        </div>
      </div>
    </SourcesProvider>
  );
}
