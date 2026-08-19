export function FilingsUploadSkeleton() {
  return (
    <div className="w-full flex-1 max-w-4xl mx-auto flex flex-col items-center mt-10 animate-fade-in-up">
      <div className="w-full p-12 border-2 border-dashed border-outline-variant rounded-xl bg-surface-container-low flex flex-col items-center justify-center gap-4 text-center animate-pulse">
        <div className="w-16 h-16 bg-surface-container-high rounded-full flex items-center justify-center mb-2"></div>
        <div className="h-6 w-48 bg-surface-container-high rounded-full"></div>
        <div className="h-4 w-64 bg-surface-container-high rounded-full"></div>
      </div>
    </div>
  );
}
