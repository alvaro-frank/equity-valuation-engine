export function HeaderSkeleton() {
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant">
      <div>
        <div className="flex items-center gap-3">
          <div className="h-10 w-48 bg-surface-container-high rounded animate-pulse"></div>
          <div className="h-6 w-24 bg-surface-container-high rounded animate-pulse"></div>
        </div>
        <div className="h-5 w-64 bg-surface-container-high rounded mt-2 animate-pulse"></div>
      </div>
    </div>
  );
}
