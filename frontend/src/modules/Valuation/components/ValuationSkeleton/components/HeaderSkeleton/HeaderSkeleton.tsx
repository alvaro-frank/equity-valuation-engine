export function HeaderSkeleton() {
  return (
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
  );
}
