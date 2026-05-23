import React from 'react';
import { useQuantitativeData, useQualitativeData, useSectorData } from '../Valuation/hooks/useValuationData';
import { DashboardView } from './DashboardView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';

interface DashboardProps {
  ticker: string;
}

export function Dashboard({ ticker }: DashboardProps) {
  const { 
    data: quantData, 
    isLoading: isLoadingQuant, 
    error: errorQuant,
    refetch: refetchQuant
  } = useQuantitativeData(ticker);

  const { 
    data: qualData, 
    isLoading: isLoadingQual, 
    error: errorQual,
    refetch: refetchQual
  } = useQualitativeData(ticker);

  // In a real scenario, we could show a global spinner if both are loading
  if (isLoadingQuant || isLoadingQual) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Elegant Error State (Option 1)
  if (errorQuant || errorQual) {
    // Extract status code from Axios error
    const getStatusCode = (err: any) => err?.response?.status;
    const statusCode = getStatusCode(errorQuant) || getStatusCode(errorQual);

    let errorTitle = `Unable to analyze ${ticker}`;
    let errorMessage = (errorQuant as any)?.response?.data?.detail || (errorQual as any)?.response?.data?.detail || errorQuant?.message || errorQual?.message || 'Our evaluation engine encountered a problem while processing this report. Please try again.';
    let errorIcon = "error_outline";

    if (statusCode === 404) {
      errorTitle = "Ticker Not Found";
      errorMessage = `We couldn't find any financial data for "${ticker}". Please check the spelling and try again.`;
      errorIcon = "search_off";
    } else if (statusCode === 429) {
      errorTitle = "Rate Limit Exceeded";
      errorMessage = "We have reached the maximum number of requests allowed by our data provider. Please wait a minute and try again.";
      errorIcon = "hourglass_empty";
    }

    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in duration-500">
        <div className="w-20 h-20 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-6">
          <span className="material-symbols-outlined text-[40px] text-error">{errorIcon}</span>
        </div>
        <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
          {errorTitle}
        </h2>
        <p className="text-body-md text-on-surface-variant max-w-md mb-8 leading-relaxed">
          {errorMessage}
        </p>
        <button 
          onClick={() => {
            if (errorQuant) refetchQuant();
            if (errorQual) refetchQual();
          }}
          className="flex items-center gap-2 px-6 py-2.5 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-all duration-200 font-label-lg font-medium hover:bg-surface-container-high active:scale-95"
        >
          <span className="material-symbols-outlined text-[18px]">refresh</span>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <DashboardView 
        ticker={ticker}
        quantData={quantData} 
        qualData={qualData} 
      />
    </ErrorBoundary>
  );
}
