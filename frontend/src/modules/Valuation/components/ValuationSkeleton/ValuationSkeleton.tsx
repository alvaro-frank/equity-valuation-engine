import { useTranslation } from 'react-i18next';

export function ValuationSkeleton() {
  const { i18n } = useTranslation();

  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 pb-12 flex flex-col animate-in fade-in duration-500">
      {/* Header Skeleton */}
      <div className="flex flex-col md:flex-row md:items-start justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6 gap-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-10 w-48 bg-surface-container-high rounded animate-pulse"></div>
            <div className="h-5 w-20 bg-surface-container-high rounded animate-pulse"></div>
          </div>
          <div className="h-4 w-64 bg-surface-container-high rounded mt-2 animate-pulse"></div>
        </div>
        
        <div className="flex items-center gap-8">
          {/* Verdict Skeleton */}
          <div className="flex items-center gap-6">
            <div className="flex flex-col items-end gap-1">
              <div className="h-4 w-20 bg-surface-container-high rounded animate-pulse"></div>
              <div className="h-10 w-32 bg-surface-container-high rounded animate-pulse mt-1"></div>
            </div>
            <div className="w-px h-14 bg-outline-variant hidden sm:block"></div>
            <div className="flex flex-col items-end gap-1">
              <div className="h-4 w-24 bg-surface-container-high rounded animate-pulse"></div>
              <div className="flex items-center gap-3 mt-1">
                <div className="h-10 w-32 bg-surface-container-high rounded animate-pulse"></div>
                <div className="h-6 w-16 bg-surface-container-high rounded animate-pulse"></div>
              </div>
            </div>
          </div>
          
          {/* Scenario Selector Skeleton */}
          <div className="h-10 w-64 bg-surface-container-high rounded-lg animate-pulse hidden lg:block"></div>
        </div>
      </div>

      {/* Main Content Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-4 flex-1">
        {/* Left Panel */}
        <div className="lg:col-span-4 space-y-6">
          <div className="h-80 bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
          <div className="h-48 bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
        </div>

        {/* Right Panel */}
        <div className="lg:col-span-8">
          <div className="h-full min-h-[400px] bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
        </div>
      </div>

      {/* Floating Toast Notification */}
      <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
        <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
        <span className="text-on-surface font-medium text-sm animate-pulse">
          {i18n.language === 'pt' ? 'A calcular Cash Flows...' : 'Calculating Cash Flows...'}
        </span>
      </div>
    </div>
  );
}
