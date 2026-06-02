import { useState } from 'react';
import { PdfUploader } from '@/common/components/PdfUploader/PdfUploader';
import { EarningsReportCard } from './components/EarningsReportCard';
import { useEarningsAnalysis } from './hooks/useEarningsAnalysis';

import { useQueryClient } from '@tanstack/react-query';

export function FilingsView({ ticker }: { ticker: string }) {
  const queryClient = useQueryClient();
  const { mutate, data: mutationData, isPending, error, reset } = useEarningsAnalysis();

  const cachedData = queryClient.getQueryData(['earnings_analysis', ticker]);
  const activeData = mutationData || cachedData;

  const handleReset = () => {
    reset();
    queryClient.removeQueries({ queryKey: ['earnings_analysis', ticker] });
  };

  const handleFileSelect = (file: File) => {
    mutate({ ticker, file });
  };

  const getErrorMessage = () => {
    if (!error) return "";
    const anyErr = error as any;
    return anyErr.response?.data?.detail || anyErr.message || "Please ensure it's a valid Earnings Report PDF and try again.";
  };

  return (
    <div className="w-full max-w-[1200px] mx-auto h-full flex flex-col">
      
      {!activeData && !error && (
        <div className="flex-1 mt-12">
          <PdfUploader onFileSelect={handleFileSelect} isUploading={isPending} />
        </div>
      )}

      {error && (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in duration-500">
          <div className="w-20 h-20 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-6">
            <span className="material-symbols-outlined text-[40px] text-error">error_outline</span>
          </div>
          <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
            Unable to analyze document
          </h2>
          <p className="text-body-md text-on-surface-variant max-w-md mb-8 leading-relaxed">
            {getErrorMessage()}
          </p>
          <button 
            onClick={handleReset}
            className="flex items-center gap-2 px-6 py-2.5 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-all duration-200 font-label-lg font-medium hover:bg-surface-container-high active:scale-95"
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span>
            Try Again
          </button>
        </div>
      )}

      {activeData && (
        <div className="flex-1 pb-10">
          <div className="flex items-center gap-3 mb-4">
            <h3 className="text-lg font-bold text-on-surface">Analysis Results</h3>
            <button 
              onClick={handleReset} 
              className="p-1.5 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant border border-outline-variant transition-colors flex items-center justify-center"
              title="Analyze Another"
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
