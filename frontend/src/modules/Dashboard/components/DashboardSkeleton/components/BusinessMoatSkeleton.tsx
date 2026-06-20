import { Skeleton } from '@/common/components/Skeleton';

export function BusinessMoatSkeleton() {
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
