import { useTranslation } from 'react-i18next';

export function ThesisSkeleton() {
  const { i18n } = useTranslation();

  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 flex flex-col gap-6 animate-in fade-in duration-500">
      {/* Header Skeleton */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-10 w-48 bg-surface-container-high rounded animate-pulse"></div>
            <div className="h-6 w-24 bg-surface-container-high rounded animate-pulse"></div>
          </div>
          <div className="h-5 w-64 bg-surface-container-high rounded mt-2 animate-pulse"></div>
        </div>
      </div>

      {/* SubNav Skeleton */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        <div className="h-9 w-32 bg-surface-container-high rounded-full animate-pulse"></div>
        <div className="h-9 w-40 bg-surface-container-high rounded-full animate-pulse"></div>
        <div className="h-9 w-36 bg-surface-container-high rounded-full animate-pulse"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
        </div>
        <div className="space-y-6">
          <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
        </div>
      </div>
    
      {/* Floating Toast Notification for drafting thesis */}
      <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
        <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
        <span className="text-on-surface font-medium text-sm animate-pulse">
          {i18n.language === 'pt' ? 'A redigir Tese de Investimento...' : 'Drafting Investment Thesis...'}
        </span>
      </div>
    </div>
  );
}
