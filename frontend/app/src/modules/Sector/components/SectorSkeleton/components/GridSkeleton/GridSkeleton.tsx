export function GridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
      <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
      <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
    </div>
  );
}
