export function FilingsHeaderSkeleton() {
  return (
    <div className="flex flex-col md:flex-row items-start justify-between gap-4 py-6 border-b border-outline-variant mb-6 w-full animate-in fade-in duration-500">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3">
          <div className="h-8 w-64 bg-surface-container-high rounded animate-pulse"></div>
          <div className="h-6 w-24 bg-surface-container-high rounded-full animate-pulse"></div>
        </div>
        <div className="flex flex-wrap items-center gap-2 mt-2">
          <div className="h-6 w-32 bg-surface-container-high rounded-full animate-pulse"></div>
          <div className="h-6 w-40 bg-surface-container-high rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  );
}
