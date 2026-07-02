import { useParams } from 'react-router-dom';
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
          <FilingsResultsHeader 
            ticker={quantData?.ticker?.symbol || ticker || ''}
            name={quantData?.ticker?.name}
            sector={quantData?.ticker?.sector}
            industry={quantData?.ticker?.industry}
          />
          <div className="mt-8">
            <AvailableFilingsGrid 
              filings={localFilings} 
              onSelectFiling={handleLocalFilingSelect} 
              isAnalyzing={isPending}
              analyzingFilingId={analyzingFilingId}
              analyzingPeriod={analyzingPeriod}
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
  return (
    <div className="w-full max-w-[1600px] mx-auto flex-1 flex flex-col">
      <div className="flex-1 pb-10">
        <FilingsResultsHeader 
          onReset={handleReset}
          ticker={activeData.ticker.symbol}
          name={activeData.ticker.name}
          sector={activeData.ticker.sector}
          industry={activeData.ticker.industry}
          periodEndDate={activeData.period_end_date}
        />
        <EarningsReportCard data={activeData} quantData={quantData} />
      </div>
    </div>
  );
}
