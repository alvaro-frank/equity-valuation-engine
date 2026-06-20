export function SubNavSkeleton() {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2">
      <div className="h-9 w-32 bg-surface-container-high rounded-full animate-pulse"></div>
      <div className="h-9 w-40 bg-surface-container-high rounded-full animate-pulse"></div>
      <div className="h-9 w-36 bg-surface-container-high rounded-full animate-pulse"></div>
    </div>
  );
}
