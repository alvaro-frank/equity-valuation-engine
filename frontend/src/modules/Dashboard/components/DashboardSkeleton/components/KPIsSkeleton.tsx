import { Skeleton } from '@/common/components/Skeleton';

export function KPIsSkeleton() {
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
