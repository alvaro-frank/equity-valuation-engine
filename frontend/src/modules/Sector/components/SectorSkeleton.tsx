interface SectorSkeletonProps {
  language: string;
}

export function SectorSkeleton({ language }: SectorSkeletonProps) {
  return (
    <div className="max-w-[1400px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
      <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
        <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
        <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
      </div>
    
      {/* Floating Toast Notification for drafting analysis */}
      <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
        <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
        <span className="text-on-surface font-medium text-sm animate-pulse">
          {language === 'pt' ? 'A redigir Análise Setorial...' : 'Drafting Sector Analysis...'}
        </span>
      </div>
    </div>
  );
}
