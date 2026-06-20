export function ContentSkeleton() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-4 flex-1">
      {/* Left Panel */}
      <div className="lg:col-span-4 space-y-6">
        <div className="h-80 bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
        <div className="h-48 bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
      </div>

      {/* Right Panel */}
      <div className="lg:col-span-8">
        <div className="h-full min-h-[400px] bg-surface-container rounded-xl border border-outline-variant animate-pulse"></div>
      </div>
    </div>
  );
}
