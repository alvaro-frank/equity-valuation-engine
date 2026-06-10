import { PdfUploader } from '@/common/components/PdfUploader/PdfUploader';
import { EarningsReportCard } from './components/EarningsReportCard';
import { FilingsErrorState } from './components/FilingsErrorState';
import { useFilingsView } from './hooks/useFilingsView';

export function FilingsView({ ticker }: { ticker: string }) {
  const { 
    t, 
    activeData, 
    isPending, 
    errorState, 
    handleFileSelect, 
    handleReset 
  } = useFilingsView(ticker);

  return (
    <div className="w-full max-w-[1200px] mx-auto h-full flex flex-col">
      
      {!activeData && !errorState && (
        <div className="flex-1 mt-12">
          <PdfUploader onFileSelect={handleFileSelect} isUploading={isPending} />
        </div>
      )}

      {errorState && (
        <FilingsErrorState errorState={errorState} onReset={handleReset} />
      )}

      {activeData && (
        <div className="flex-1 pb-10">
          <div className="flex items-center gap-3 mb-4">
            <h3 className="text-lg font-bold text-on-surface">{t('filings.results')}</h3>
            <button 
              onClick={handleReset} 
              className="p-1.5 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant transition-colors flex items-center justify-center"
              title={t('filings.analyze_another')}
            >
              <span className="material-symbols-outlined text-[18px]">refresh</span>
            </button>
          </div>
          <EarningsReportCard data={activeData} />
        </div>
      )}
      
    </div>
  );
}
