export function FilingsGridSkeleton() {
  return (
    <div className="mb-10 animate-fade-in-up">
      <div className="space-y-8">
        <div>
          <div className="h-5 w-48 bg-surface-container-high rounded mb-3 animate-pulse"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-[88px] bg-surface-container-high rounded-xl border border-outline-variant animate-pulse"></div>
            ))}
          </div>
        </div>

        <div>
          <div className="h-5 w-48 bg-surface-container-high rounded mb-3 animate-pulse"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-[88px] bg-surface-container-high rounded-xl border border-outline-variant animate-pulse"></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
