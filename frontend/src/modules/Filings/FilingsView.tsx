import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { SubNav } from '@/common/components/SubNav';
import { TranscriptView } from '@/modules/Filings/components/TranscriptView';
import { PdfUploader } from '@/modules/Filings/components/PdfUploader';
import { EarningsReportCard } from '@/modules/Filings/components/EarningsReportCard';
import { AvailableFilingsGrid } from '@/modules/Filings/components/AvailableFilingsGrid';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { useFilingsView } from '@/modules/Filings/hooks/useFilingsView';
import { FilingsResultsHeader } from '@/modules/Filings/components/FilingsResultsHeader';
import { FilingsSkeleton } from '@/modules/Filings/components/FilingsSkeleton';

// --- Main Component ---

export function FilingsView() {
  const { ticker } = useParams<{ ticker: string }>();
  const { 
    isInitialLoading,
    validationErrorState,
    activeData, 
    quantData,
    localFilings,
    isPending,
    analyzingFilingId,
    analyzingPeriod,
    errorState, 
    handleFileSelect,
    handleLocalFilingSelect,
    handleReset 
  } = useFilingsView(ticker!);

  const [activeTab, setActiveTab] = useState<'analysis' | 'transcript'>('analysis');

  // 1. Validation Error State
  if (validationErrorState) {
    return <ApiErrorState errorState={validationErrorState} onRetry={handleReset} />;
  }

  // 2. Loading State (Verifying Ticker & Fetching Data)
  if (isInitialLoading && !activeData) {
    return <FilingsSkeleton />;
  }

  // 3. API Error State
  if (errorState) {
    return <ApiErrorState errorState={errorState} onRetry={handleReset} />;
  }

  // 2. Empty / Upload State
  if (!activeData) {
    return (
      <div className="w-full max-w-[1600px] mx-auto flex-1 flex flex-col">
        <div className="flex-1 pb-10">
          <div className="pt-6 mb-6">
            <FilingsResultsHeader 
              ticker={quantData?.ticker?.symbol || ticker || ''}
              name={quantData?.ticker?.name}
              sector={quantData?.ticker?.sector}
              industry={quantData?.ticker?.industry}
            />
          </div>
          <div className="mt-8">
            <AvailableFilingsGrid 
              filings={localFilings} 
              onSelectFiling={handleLocalFilingSelect} 
              isAnalyzing={isPending}
              analyzingFilingId={analyzingFilingId}
            />
            
            {localFilings.length > 0 && (
              <hr className="border-t border-outline-variant my-10" />
            )}

            <PdfUploader 
              onFileSelect={handleFileSelect} 
              isUploading={isPending && !analyzingFilingId} 
              isDisabled={isPending}
            />
          </div>
        </div>
      </div>
    );
  }

  // 3. Success / Results State
  const tabs = [
    { id: 'analysis', label: 'Analysis', icon: 'analytics' },
    { id: 'transcript', label: 'Transcript', icon: 'record_voice_over' }
  ];

  return (
    <div className="w-full max-w-[1600px] mx-auto flex-1 flex flex-col pb-12">
      <div className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 pt-6 pb-4 flex flex-col gap-6 -mx-4 px-4 sm:-mx-8 sm:px-8 border-b border-outline-variant/20 mb-6">
        <FilingsResultsHeader 
          onReset={handleReset}
          ticker={activeData.ticker.symbol}
          name={activeData.ticker.name}
          sector={activeData.ticker.sector}
          industry={activeData.ticker.industry}
          periodEndDate={activeData.period_end_date}
        />
        <SubNav 
          tabs={tabs} 
          activeTabId={activeTab} 
          onTabChange={(id) => setActiveTab(id as 'analysis' | 'transcript')} 
        />
      </div>
      
      <div className="bg-surface-container-low border border-outline-variant rounded-xl p-6 min-h-[500px]">
        {activeTab === 'analysis' ? (
          <EarningsReportCard data={activeData} quantData={quantData} />
        ) : (
          <TranscriptView transcript={activeData.transcript || []} />
        )}
      </div>
    </div>
  );
}
