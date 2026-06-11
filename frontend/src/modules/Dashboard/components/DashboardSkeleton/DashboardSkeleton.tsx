import { useTranslation } from 'react-i18next';
import { Skeleton } from '@/common/components/Skeleton';

function HeaderSkeleton() {
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-1">
      <div className="flex items-center gap-3">
        {/* Title */}
        <Skeleton className="h-10 w-64 rounded-md" />
        {/* Badge */}
        <Skeleton className="h-6 w-16 rounded-full" />
      </div>
      <div className="flex flex-col items-end gap-2">
        {/* Live Pricing tag */}
        <Skeleton className="h-4 w-32" />
        {/* Price */}
        <Skeleton className="h-10 w-48 rounded-md" />
      </div>
    </div>
  );
}

function KPIsSkeleton() {
  return (
    <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="bg-surface-container-low border border-outline-variant p-3 flex flex-col h-28 rounded-xl overflow-hidden">
          <div className="flex justify-between items-start">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-4 rounded-full" />
          </div>
          <div className="mt-auto">
            <Skeleton className="h-6 w-32 mb-2" />
            <Skeleton className="h-3 w-16" />
          </div>
        </div>
      ))}
    </section>
  );
}

function BusinessMoatSkeleton() {
  return (
    <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
      {/* Left: Business Strategy */}
      <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-outline-variant">
          <Skeleton className="h-5 w-64" />
        </div>
        <div className="p-6 space-y-4">
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-[90%]" />
            <Skeleton className="h-4 w-[95%]" />
          </div>
          
          <div className="grid grid-cols-3 gap-4 pt-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-surface-container-lowest p-3 border border-outline-variant/50 flex flex-col h-48 rounded-lg">
                <Skeleton className="h-4 w-24 mb-4" />
                <div className="space-y-2">
                  <Skeleton className="h-3 w-full" />
                  <Skeleton className="h-3 w-[85%]" />
                  <Skeleton className="h-3 w-[90%]" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right: Leadership & Governance */}
      <div className="bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-outline-variant">
          <Skeleton className="h-5 w-48" />
        </div>
        <div className="p-4 flex-1 flex flex-col space-y-6">
          <div className="flex items-center gap-4">
            <Skeleton className="h-12 w-12 rounded-full shrink-0" />
            <div className="space-y-2 w-full">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-3 w-24" />
            </div>
          </div>
          <div className="space-y-2">
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-3 w-[90%]" />
            <Skeleton className="h-3 w-[95%]" />
          </div>
        </div>
      </div>
    </section>
  );
}

function LoadingToast() {
  const { t } = useTranslation();
  return (
    <div className="fixed bottom-6 right-6 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
      <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
      <span className="text-on-surface font-medium text-sm animate-pulse">
        {t('dashboard.loading_filings')}
      </span>
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap">
      <HeaderSkeleton />
      <KPIsSkeleton />
      <BusinessMoatSkeleton />
      <LoadingToast />
    </div>
  );
}
