
import { useParams } from 'react-router-dom';
import { PdfUploader } from './components/PdfUploader';
import { EarningsReportCard } from './components/EarningsReportCard';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { useFilingsView } from './hooks/useFilingsView';
import { FilingsResultsHeader } from './components/FilingsResultsHeader';

// --- Main Component ---

export function FilingsView() {
  const { ticker } = useParams<{ ticker: string }>();
  const { 
    activeData, 
    quantData,
    isPending, 
    errorState, 
    handleFileSelect, 
    handleReset 
  } = useFilingsView(ticker!);

  // 1. Error State
  if (errorState) {
    return <ApiErrorState errorState={errorState} onRetry={handleReset} />;
  }

  // 2. Empty / Upload State
  if (!activeData) {
    return (
      <div className="w-full max-w-[1200px] mx-auto h-full flex flex-col">
        <div className="flex-1 mt-12">
          <PdfUploader onFileSelect={handleFileSelect} isUploading={isPending} />
        </div>
      </div>
    );
  }

  // 3. Success / Results State
  return (
    <div className="w-full max-w-[1200px] mx-auto h-full flex flex-col">
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
